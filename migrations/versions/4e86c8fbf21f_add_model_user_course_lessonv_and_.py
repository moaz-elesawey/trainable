"""add model user_course_lessonv and inhance some models

Revision ID: 4e86c8fbf21f
Revises: d95962308464
Create Date: 2024-10-19 12:40:27.043756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e86c8fbf21f'
down_revision = 'd95962308464'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_course_lessons',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('course_id', sa.UUID(), nullable=False),
    sa.Column('lesson_id', sa.UUID(), nullable=False),
    sa.Column('first_access_at', sa.DateTime(), nullable=False),
    sa.Column('last_access_at', sa.DateTime(), nullable=False),
    sa.Column('is_accessed', sa.Boolean(), nullable=False),
    sa.Column('is_marked_completed', sa.Boolean(), nullable=False),
    sa.Column('is_marked_skiped', sa.Boolean(), nullable=False),
    sa.Column('mark_completed_at', sa.DateTime(), nullable=True),
    sa.Column('mark_skiped_at', sa.DateTime(), nullable=True),
    sa.Column('opened_at', sa.DateTime(), nullable=True),
    sa.Column('closed_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ),
    sa.ForeignKeyConstraint(['lesson_id'], ['lessons.lesson_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('user_id', 'course_id', 'lesson_id')
    )
    with op.batch_alter_table('assessments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('duration_in_minutes', sa.Integer(), nullable=True))

    with op.batch_alter_table('course_lessons', schema=None) as batch_op:
        batch_op.add_column(sa.Column('index', sa.Integer(), nullable=True))

    with op.batch_alter_table('user_assessment_questions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('opened_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('closed_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_assessment_questions', schema=None) as batch_op:
        batch_op.drop_column('closed_at')
        batch_op.drop_column('opened_at')

    with op.batch_alter_table('course_lessons', schema=None) as batch_op:
        batch_op.drop_column('index')

    with op.batch_alter_table('assessments', schema=None) as batch_op:
        batch_op.drop_column('duration_in_minutes')

    op.drop_table('user_course_lessons')
    # ### end Alembic commands ###
