"""empty message

Revision ID: 7a109c09b1eb
Revises: 
Create Date: 2020-10-15 13:41:16.914563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a109c09b1eb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Smit_Shablon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=140), nullable=True),
    sa.Column('slug', sa.String(length=140), nullable=True),
    sa.Column('TimeFrom', sa.String(), nullable=False),
    sa.Column('TimeTo', sa.String(), nullable=False),
    sa.Column('triggerStart', sa.Integer(), nullable=False),
    sa.Column('triggerStop', sa.Integer(), nullable=False),
    sa.Column('orderStopIV', sa.Integer(), nullable=False),
    sa.Column('orderStopObiem', sa.Integer(), nullable=False),
    sa.Column('risk', sa.Integer(), nullable=False),
    sa.Column('timeToClose', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Smit_Shablon')
    # ### end Alembic commands ###
