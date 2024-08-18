from marshmallow import Schema, fields
from uuid import UUID

class UserSchema(Schema):
    id = fields.String()  # UUIDs as strings
    username = fields.String()
    email = fields.String()
    is_active = fields.Boolean()
    role = fields.String()
