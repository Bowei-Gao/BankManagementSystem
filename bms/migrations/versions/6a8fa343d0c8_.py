"""empty message

Revision ID: 6a8fa343d0c8
Revises: fa287be843af
Create Date: 2020-06-20 22:53:08.818225

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6a8fa343d0c8'
down_revision = 'fa287be843af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('loan', sa.Column('customer_id', sa.Integer(), nullable=True))
    op.drop_constraint('loan_ibfk_1', 'loan', type_='foreignkey')
    op.create_foreign_key(None, 'loan', 'customer', ['customer_id'], ['cusID'])
    op.drop_column('loan', 'accounts_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('loan', sa.Column('accounts_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'loan', type_='foreignkey')
    op.create_foreign_key('loan_ibfk_1', 'loan', 'accounts', ['accounts_id'], ['accountID'], ondelete='CASCADE')
    op.drop_column('loan', 'customer_id')
    # ### end Alembic commands ###