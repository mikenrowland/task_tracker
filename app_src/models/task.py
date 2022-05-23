from models.base import BaseModel, fields


class Task(BaseModel):
    title = fields.CharField(max_length=226, unique=True)
    description = fields.CharField(max_length=456)
    completed = fields.BooleanField(default=False)
    completed_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return self.title
