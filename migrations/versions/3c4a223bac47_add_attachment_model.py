"""Add attachment model

Revision ID: 3c4a223bac47
Revises: 4e86c8fbf21f
Create Date: 2024-10-22 12:42:14.564346

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3c4a223bac47'
down_revision = '4e86c8fbf21f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attachments',
    sa.Column('attachment_id', sa.UUID(), nullable=False),
    sa.Column('course_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('old_filename', sa.Text(), nullable=False),
    sa.Column('new_filename', sa.Text(), nullable=False),
    sa.Column('file_path', sa.Text(), nullable=False),
    sa.Column('file_data', postgresql.BYTEA(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ),
    sa.PrimaryKeyConstraint('attachment_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('attachments')
    # ### end Alembic commands ###
