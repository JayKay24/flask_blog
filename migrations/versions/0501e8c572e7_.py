"""empty message

Revision ID: 0501e8c572e7
Revises: 
Create Date: 2017-05-27 13:56:27.184134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0501e8c572e7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('entry', sa.Column('status', sa.SmallInteger(), server_default='0'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('entry', 'status')
    # ### end Alembic commands ###
