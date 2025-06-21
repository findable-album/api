from tortoise import Model, fields
from tortoise.contrib.postgres.fields import ArrayField


class Image(Model):
    id = fields.IntField(pk=True)
    path = fields.CharField(max_length=255, unique=True)
    filename = fields.CharField(max_length=255)
    description = fields.TextField()
    tags = ArrayField(element_type='text')
    description_chosung = fields.CharField(max_length=255, null=True)
    tags_chosung = ArrayField(element_type='text', null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
