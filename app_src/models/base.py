from tortoise.models import Model
from tortoise import fields


class BaseModel(Model):
    id = fields.UUIDField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)