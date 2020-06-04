"""empty message

Revision ID: 2d2f5730e25b
Revises: 671f96dc8ae5
Create Date: 2020-06-03 15:56:47.342513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d2f5730e25b'
down_revision = '671f96dc8ae5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'item_list', type_='foreignkey')
    op.create_foreign_key(None, 'item_list', 'user', ['owner_id'], ['id'])
    op.drop_column('item_list', 'owner')
    op.add_column('user', sa.Column('password_hash', sa.String(length=128), nullable=False))
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.VARCHAR(), nullable=False))
    op.drop_column('user', 'password_hash')
    op.add_column('item_list', sa.Column('owner', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'item_list', type_='foreignkey')
    op.create_foreign_key(None, 'item_list', 'user', ['owner'], ['id'])
    # ### end Alembic commands ###
