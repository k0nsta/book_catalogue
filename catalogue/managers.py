from django.db import models


class CustomQuerySet(models.QuerySet):
    """
    Change default physical delete from DB. Storage is cheap, rather
    to save for future cases than lost data
    """
    def delete(self, **kwargs):
        return self.update(is_void=True)


class CustomManager(models.Manager):
    """
    According to principe of avoiding business logic from view
    template, adedd custom methods for default manager
    """
    queryset = CustomQuerySet

    def get_queryset(self, exclude_void=True):
        q = self.queryset(self.model)
        q = q.all()
        if exclude_void:
            q = q.exclude(is_void=True)
        return q

    def get_active(self):
        return self.get_queryset().filter(is_active=True)

    def get_all_objects_include_void(self):
        return self.get_queryset(exclude_void=False)
