from rest_framework import serializers

from .models import Tag, Task


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

    def validate_name(self, value):
        normalized = value.strip()
        if not normalized:
            raise serializers.ValidationError('Tag name cannot be empty.')

        queryset = Tag.objects.filter(name__iexact=normalized)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('A tag with this name already exists.')

        return normalized


class TagNestedWriteSerializer(serializers.Serializer):
    """Accept tag name when creating/updating tasks."""

    name = serializers.CharField(max_length=100)

    def validate_name(self, value):
        normalized = value.strip()
        if not normalized:
            raise serializers.ValidationError('Tag name cannot be empty.')
        return normalized


class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        source='tags',
        write_only=True,
        required=False,
    )
    tag_names = TagNestedWriteSerializer(
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'created_at',
            'tags',
            'tag_ids',
            'tag_names',
        ]
        read_only_fields = ['id', 'created_at']

    def _resolve_tags(self, tag_ids=None, tag_names=None):
        tags = []
        if tag_ids:
            tags.extend(tag_ids)

        if tag_names:
            for item in tag_names:
                name = item['name']
                tag = Tag.objects.filter(name__iexact=name).first()
                if tag is None:
                    tag = Tag.objects.create(name=name)
                tags.append(tag)

        return list(dict.fromkeys(tags))

    def create(self, validated_data):
        tag_ids = validated_data.pop('tags', [])
        tag_names = validated_data.pop('tag_names', [])
        task = Task.objects.create(**validated_data)
        tags = self._resolve_tags(tag_ids=tag_ids, tag_names=tag_names)
        if tags:
            task.tags.set(tags)
        return task

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tags', None)
        tag_names = validated_data.pop('tag_names', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tag_ids is not None or tag_names is not None:
            tags = self._resolve_tags(
                tag_ids=tag_ids or [],
                tag_names=tag_names or [],
            )
            instance.tags.set(tags)

        return instance
