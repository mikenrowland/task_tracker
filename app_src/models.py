from tortoise.models import Model
from tortoise import fields


class Task(Model):
    id = fields.UUIDField(pk=True)
    title = fields.CharField(max_length=226, unique=True)
    description = fields.CharField(max_length=456)
    completed = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    completed_at = fields.DatetimeField(auto_now=True)
