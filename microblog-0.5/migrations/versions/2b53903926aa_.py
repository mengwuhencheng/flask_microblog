"""empty message

Revision ID: 2b53903926aa
Revises: db72770ac390
Create Date: 2016-10-26 20:57:43.250849

"""

# revision identifiers, used by Alembic.
revision = '2b53903926aa'
down_revision = 'db72770ac390'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('body_html', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'body_html')
    ### end Alembic commands ###
