from models.base import BaseModel, fields


class UserRegister(BaseModel):
    email = fields.CharField(max_length=125, unique=True)
    first_name = fields.CharField(max_length=125)
    last_name = fields.CharField(max_length=125)
    password = fields.CharField(max_length=1000)
