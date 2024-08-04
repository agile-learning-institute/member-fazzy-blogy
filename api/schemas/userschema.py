from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    is_active = fields.Bool()
    role = fields.Str()

# Create schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)
