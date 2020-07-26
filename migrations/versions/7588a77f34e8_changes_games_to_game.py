"""changes Games to Game

Revision ID: 7588a77f34e8
Revises: 7867bea3ee7e
Create Date: 2020-07-26 01:04:21.426754

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7588a77f34e8'
down_revision = '7867bea3ee7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=140), nullable=True),
    sa.Column('platform', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_game_timestamp'), 'game', ['timestamp'], unique=False)
    op.drop_index('ix_games_timestamp', table_name='games')
    op.drop_table('games')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('games',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', mysql.VARCHAR(length=140), nullable=True),
    sa.Column('platform', mysql.VARCHAR(length=140), nullable=True),
    sa.Column('timestamp', mysql.DATETIME(), nullable=True),
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='games_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_games_timestamp', 'games', ['timestamp'], unique=False)
    op.drop_index(op.f('ix_game_timestamp'), table_name='game')
    op.drop_table('game')
    # ### end Alembic commands ###
