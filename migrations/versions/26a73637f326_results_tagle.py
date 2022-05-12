"""results tagle

Revision ID: 26a73637f326
Revises: c8eca14265fe
Create Date: 2022-05-11 16:25:44.167572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26a73637f326'
down_revision = 'c8eca14265fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('result', sa.Column('clear_time', sa.Integer(), nullable=True))
    op.add_column('result', sa.Column('clear_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('result', 'clear_date')
    op.drop_column('result', 'clear_time')
    # ### end Alembic commands ###