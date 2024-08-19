from marshmallow import Schema, fields

class CommentSchema(Schema):
    id = fields.UUID(dump_only=True)
    blog_post_id = fields.UUID(required=True)
    user_id = fields.UUID(required=True)
    comment = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
