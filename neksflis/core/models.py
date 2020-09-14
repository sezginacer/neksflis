import uuid as uuid
from django.db import models


class StarterModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
