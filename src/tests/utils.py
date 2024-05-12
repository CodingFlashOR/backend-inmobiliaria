from django.db.models import Model, QuerySet


def get_empty_queryset(model: Model) -> QuerySet:
    """
    This function returns an empty queryset for the given model.
    """

    return model.objects.none()
