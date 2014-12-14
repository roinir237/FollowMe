"""add unique contraint on tweet url

Revision ID: 564c09eaecc6
Revises: 1c89b3661a0
Create Date: 2014-12-13 13:38:43.325792

"""

# revision identifiers, used by Alembic.
revision = '564c09eaecc6'
down_revision = '1c89b3661a0'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_unique_constraint("uq_tweets_url", "tweets", ["url"])


def downgrade():
    op.drop_contraint("uq_tweets_url",
                      "tweets",
                       "unique")
