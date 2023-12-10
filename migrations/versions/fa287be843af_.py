"""empty message

Revision ID: fa287be843af
Revises: 
Create Date: 2020-06-20 21:17:26.423844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa287be843af'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bank',
    sa.Column('bankId', sa.Integer(), nullable=False),
    sa.Column('bankname', sa.String(length=20), nullable=True),
    sa.Column('city', sa.String(length=20), nullable=False),
    sa.Column('money', sa.Float(asdecimal=True), nullable=False),
    sa.PrimaryKeyConstraint('bankId')
    )
    op.create_table('department',
    sa.Column('departID', sa.Integer(), nullable=False),
    sa.Column('departname', sa.String(length=20), nullable=False),
    sa.Column('departtype', sa.String(length=15), nullable=True),
    sa.Column('manager', sa.String(length=18), nullable=False),
    sa.Column('bank', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['bank'], ['bank.bankId'], ),
    sa.PrimaryKeyConstraint('departID')
    )
    op.create_index(op.f('ix_department_bank'), 'department', ['bank'], unique=False)
    op.create_table('employee',
    sa.Column('empID', sa.Integer(), nullable=False),
    sa.Column('empname', sa.String(length=20), nullable=False),
    sa.Column('empphone', sa.String(length=11), nullable=True),
    sa.Column('empaddr', sa.String(length=50), nullable=True),
    sa.Column('emptype', sa.String(length=1), nullable=True),
    sa.Column('empstart', sa.DateTime(), nullable=False),
    sa.Column('depart', sa.Integer(), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('bank_id', sa.Integer(), nullable=True),
    sa.CheckConstraint("(`emptype` in (_utf8mb4'0',_utf8mb4'1'))"),
    sa.ForeignKeyConstraint(['bank_id'], ['bank.bankId'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['depart'], ['department.departID'], ),
    sa.PrimaryKeyConstraint('empID')
    )
    op.create_index(op.f('ix_employee_depart'), 'employee', ['depart'], unique=False)
    op.create_table('customer',
    sa.Column('cusID', sa.Integer(), nullable=False),
    sa.Column('cusname', sa.String(length=10), nullable=False),
    sa.Column('cusphone', sa.String(length=11), nullable=False),
    sa.Column('address', sa.String(length=50), nullable=True),
    sa.Column('contact_phone', sa.String(length=11), nullable=False),
    sa.Column('contact_name', sa.String(length=10), nullable=False),
    sa.Column('contact_Email', sa.String(length=20), nullable=True),
    sa.Column('relation', sa.String(length=10), nullable=False),
    sa.Column('loanres', sa.Integer(), nullable=True),
    sa.Column('accres', sa.Integer(), nullable=True),
    sa.Column('employee_id', sa.Integer(), nullable=True),
    sa.Column('bank_id', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['accres'], ['employee.empID'], ),
    sa.ForeignKeyConstraint(['bank_id'], ['bank.bankId'], ),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.empID'], ),
    sa.ForeignKeyConstraint(['loanres'], ['employee.empID'], ),
    sa.PrimaryKeyConstraint('cusID')
    )
    op.create_index(op.f('ix_customer_accres'), 'customer', ['accres'], unique=False)
    op.create_index(op.f('ix_customer_loanres'), 'customer', ['loanres'], unique=False)
    op.create_table('accounts',
    sa.Column('accountID', sa.Integer(), nullable=False),
    sa.Column('money', sa.Float(asdecimal=True), nullable=False),
    sa.Column('settime', sa.DateTime(), nullable=True),
    sa.Column('accounttype', sa.String(length=10), nullable=True),
    sa.Column('accountNumber', sa.String(length=30), nullable=True),
    sa.Column('bank_id', sa.Integer(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('employee_id', sa.Integer(), nullable=True),
    sa.CheckConstraint("(`accounttype` in ('储蓄账户','支票账户'))"),
    sa.ForeignKeyConstraint(['bank_id'], ['bank.bankId'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.cusID'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.empID'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('accountID'),
    sa.UniqueConstraint('accountNumber')
    )
    op.create_table('checkacc',
    sa.Column('accountID', sa.Integer(), nullable=False),
    sa.Column('overdraft', sa.Float(asdecimal=True), nullable=True),
    sa.ForeignKeyConstraint(['accountID'], ['accounts.accountID'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('accountID')
    )
    op.create_table('cusforacc',
    sa.Column('accountID', sa.Integer(), nullable=False),
    sa.Column('bank', sa.Integer(), nullable=True),
    sa.Column('cusID', sa.Integer(), nullable=False),
    sa.Column('visit', sa.DateTime(), nullable=True),
    sa.Column('accounttype', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['accountID'], ['accounts.accountID'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['bank'], ['bank.bankId'], ),
    sa.ForeignKeyConstraint(['cusID'], ['customer.cusID'], ),
    sa.PrimaryKeyConstraint('accountID', 'cusID')
    )
    op.create_index('UK', 'cusforacc', ['bank', 'cusID', 'accounttype'], unique=False)
    op.create_index(op.f('ix_cusforacc_cusID'), 'cusforacc', ['cusID'], unique=False)
    op.create_table('loan',
    sa.Column('loanID', sa.Integer(), nullable=False),
    sa.Column('money', sa.Float(asdecimal=True), nullable=True),
    sa.Column('bank', sa.Integer(), nullable=True),
    sa.Column('state', sa.String(length=1), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('accounts_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['accounts_id'], ['accounts.accountID'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['bank'], ['bank.bankId'], ),
    sa.PrimaryKeyConstraint('loanID')
    )
    op.create_index(op.f('ix_loan_bank'), 'loan', ['bank'], unique=False)
    op.create_table('saveacc',
    sa.Column('accountID', sa.Integer(), nullable=False),
    sa.Column('interestrate', sa.Float(), nullable=True),
    sa.Column('savetype', sa.String(length=1), nullable=True),
    sa.ForeignKeyConstraint(['accountID'], ['accounts.accountID'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('accountID')
    )
    op.create_table('cusforloan',
    sa.Column('loanID', sa.Integer(), nullable=False),
    sa.Column('cusID', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cusID'], ['customer.cusID'], ),
    sa.ForeignKeyConstraint(['loanID'], ['loan.loanID'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('loanID', 'cusID')
    )
    op.create_index(op.f('ix_cusforloan_cusID'), 'cusforloan', ['cusID'], unique=False)
    op.create_table('payinfo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('loanID', sa.Integer(), nullable=False),
    sa.Column('cusID', sa.Integer(), nullable=False),
    sa.Column('money', sa.Float(asdecimal=True), nullable=False),
    sa.Column('paytime', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['cusID'], ['customer.cusID'], ),
    sa.ForeignKeyConstraint(['loanID'], ['loan.loanID'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payinfo_cusID'), 'payinfo', ['cusID'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_payinfo_cusID'), table_name='payinfo')
    op.drop_table('payinfo')
    op.drop_index(op.f('ix_cusforloan_cusID'), table_name='cusforloan')
    op.drop_table('cusforloan')
    op.drop_table('saveacc')
    op.drop_index(op.f('ix_loan_bank'), table_name='loan')
    op.drop_table('loan')
    op.drop_index(op.f('ix_cusforacc_cusID'), table_name='cusforacc')
    op.drop_index('UK', table_name='cusforacc')
    op.drop_table('cusforacc')
    op.drop_table('checkacc')
    op.drop_table('accounts')
    op.drop_index(op.f('ix_customer_loanres'), table_name='customer')
    op.drop_index(op.f('ix_customer_accres'), table_name='customer')
    op.drop_table('customer')
    op.drop_index(op.f('ix_employee_depart'), table_name='employee')
    op.drop_table('employee')
    op.drop_index(op.f('ix_department_bank'), table_name='department')
    op.drop_table('department')
    op.drop_table('bank')
    # ### end Alembic commands ###
