"""Fixed relationship conflicts

Revision ID: c1b97e94e75a
Revises: ef88d18af0df
Create Date: 2024-08-02 04:38:07.818475

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1b97e94e75a'
down_revision: Union[str, None] = 'ef88d18af0df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blog_posts', sa.Column('content', sa.Text(), nullable=False))
    op.add_column('blog_posts', sa.Column('author_id', sa.UUID(), nullable=False))
    op.alter_column('blog_posts', 'title',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=200),
               existing_nullable=False)
    op.drop_constraint('blog_posts_user_id_fkey', 'blog_posts', type_='foreignkey')
    op.create_foreign_key(None, 'blog_posts', 'users', ['author_id'], ['id'])
    op.drop_column('blog_posts', 'post')
    op.drop_column('blog_posts', 'user_id')
    op.drop_column('blog_posts', 'summary')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blog_posts', sa.Column('summary', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.add_column('blog_posts', sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False))
    op.add_column('blog_posts', sa.Column('post', sa.TEXT(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'blog_posts', type_='foreignkey')
    op.create_foreign_key('blog_posts_user_id_fkey', 'blog_posts', 'users', ['user_id'], ['id'])
    op.alter_column('blog_posts', 'title',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
    op.drop_column('blog_posts', 'author_id')
    op.drop_column('blog_posts', 'content')
    # ### end Alembic commands ###
