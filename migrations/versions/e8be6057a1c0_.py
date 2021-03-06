"""empty message

Revision ID: e8be6057a1c0
Revises: 017c253a075f
Create Date: 2020-04-18 11:23:59.885431

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8be6057a1c0'
down_revision = '017c253a075f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('video_url', sa.String(length=255), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('board_id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['teacher.id'], ),
    sa.ForeignKeyConstraint(['board_id'], ['board.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['student.id'], ),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    op.drop_table('course')
    # ### end Alembic commands ###
