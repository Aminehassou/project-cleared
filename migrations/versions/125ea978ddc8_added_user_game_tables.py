"""Added user_game tables

Revision ID: 125ea978ddc8
Revises: 4a11bb603dd8
Create Date: 2020-08-17 03:15:53.375624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '125ea978ddc8'
down_revision = '4a11bb603dd8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('game', sa.Column('image_id', sa.String(length=255), nullable=False))
    op.create_unique_constraint(None, 'game', ['image_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'game', type_='unique')
    op.drop_column('game', 'image_id')
    # ### end Alembic commands ###