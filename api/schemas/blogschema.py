from marshmallow import Schema, fields

class BlogPostSchema(Schema):
    id = fields.UUID(required=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    created_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S', required=True)
    updated_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S', allow_none=True)
    author_id = fields.UUID(required=True)
