import django_filters

from .models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Task.Status.choices)
    tag = django_filters.CharFilter(field_name='tags__name', lookup_expr='iexact')

    class Meta:
        model = Task
        fields = ['status', 'tag']
