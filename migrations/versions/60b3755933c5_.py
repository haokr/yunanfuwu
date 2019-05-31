"""empty message

Revision ID: 60b3755933c5
Revises: e5a2494c66e0
Create Date: 2019-05-31 21:14:18.422470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60b3755933c5'
down_revision = 'e5a2494c66e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('equipment_report_log', sa.Column('describe', sa.String(length=30), nullable=True))
    op.add_column('ui_report_log', sa.Column('describe', sa.String(length=30), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ui_report_log', 'describe')
    op.drop_column('equipment_report_log', 'describe')
    # ### end Alembic commands ###
