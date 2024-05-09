"""empty message

Revision ID: 2d532d0f8a92
Revises: 1d75ac0d2ebf
Create Date: 2024-05-09 15:28:01.091778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d532d0f8a92'
down_revision = '1d75ac0d2ebf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fav_character',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('character_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('user_id', 'character_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fav_character')
    # ### end Alembic commands ###