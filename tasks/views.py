from rest_framework import viewsets

from .filters import TaskFilter
from .models import Tag, Task
from .serializers import TagSerializer, TaskSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.prefetch_related('tags').all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
