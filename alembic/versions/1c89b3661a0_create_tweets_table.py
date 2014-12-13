"""create tweets table

Revision ID: 1c89b3661a0
Revises: 
Create Date: 2014-12-12 23:57:20.534154

"""

# revision identifiers, used by Alembic.
revision = '1c89b3661a0'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
     op.create_table(
        'tweets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('url', sa.String(100)),
        sa.Column('likes', sa.Integer),
        sa.Column('posted', sa.DateTime),
    )

def downgrade():
    op.drop_table('tweets')
