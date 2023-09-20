"""Rename model

Revision ID: 56eb9e3ec722
Revises: f78e86fdcbcf
Create Date: 2023-09-20 13:17:52.343591

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56eb9e3ec722'
down_revision = 'f78e86fdcbcf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    mmr_table = op.create_table('modelmeetingroom',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )

    op.drop_table('meetingroom')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('meetingroom',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )

    op.drop_table('modelmeetingroom')
    # ### end Alembic commands ###
