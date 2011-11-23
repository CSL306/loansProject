from djangorestframework.views import ModelView
from djangorestframework.mixins import ReadModelMixin, InstanceMixin

class InstanceReadOnlyModelView(InstanceMixin, ReadModelMixin, ModelView):
    """A view which provides default operations for read against a model instance."""
    _suffix = 'Instance'
