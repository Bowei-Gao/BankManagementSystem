# coding: utf-8
from datetime import datetime

from app.config import db


class Account(db.Model):
    __tablename__ = 'accounts'
    __table_args__ = (
        db.CheckConstraint("(`accounttype` in ('储蓄账户','支票账户'))"),
    )

    accountID = db.Column(db.Integer(), primary_key=True)
    money = db.Column(db.Float(asdecimal=True), nullable=False)
    settime = db.Column(db.DateTime)
    accounttype = db.Column(db.String(10))
    accountNumber = db.Column(db.String(30), unique=True)
    bank_id = db.Column(db.ForeignKey('bank.bankId', ondelete='CASCADE'))
    bank = db.relationship('Bank', primaryjoin='Account.bank_id == Bank.bankId',
                           backref='bank_account')
    customer_id = db.Column(db.ForeignKey('customer.cusID', ondelete='CASCADE'), nullable=True)  # 关联客户
    customer = db.relationship('Customer', primaryjoin='Customer.cusID == Account.customer_id',
                               backref='account_customers')

    employee_id = db.Column(db.ForeignKey('employee.empID', ondelete='CASCADE'), nullable=True)  # 关联开卡人
    employee = db.relationship('Employee', primaryjoin='Employee.empID == Account.employee_id',
                               backref='account_employee')


class Checkacc(Account):
    __tablename__ = 'checkacc'

    accountID = db.Column(db.ForeignKey('accounts.accountID', ondelete='CASCADE'), primary_key=True)
    overdraft = db.Column(db.Float(asdecimal=True))


class Saveacc(Account):
    __tablename__ = 'saveacc'

    accountID = db.Column(db.ForeignKey('accounts.accountID', ondelete='CASCADE'), primary_key=True)
    interestrate = db.Column(db.Float)
    savetype = db.Column(db.String(1))


class Bank(db.Model):
    __tablename__ = 'bank'
    bankId = db.Column(db.Integer(), primary_key=True)
    bankname = db.Column(db.String(20))
    city = db.Column(db.String(20), nullable=False)
    money = db.Column(db.Float(asdecimal=True), nullable=False)


class Cusforacc(db.Model):
    __tablename__ = 'cusforacc'
    __table_args__ = (
        db.Index('UK', 'bank', 'cusID', 'accounttype'),
    )

    accountID = db.Column(db.ForeignKey('accounts.accountID', ondelete='CASCADE'), primary_key=True, nullable=False)
    bank = db.Column(db.ForeignKey('bank.bankId'))
    cusID = db.Column(db.ForeignKey('customer.cusID'), primary_key=True, nullable=False, index=True)
    visit = db.Column(db.DateTime)
    accounttype = db.Column(db.String(10))

    account = db.relationship('Account', primaryjoin='Cusforacc.accountID == Account.accountID', backref='cusforaccs')
    bank1 = db.relationship('Bank', primaryjoin='Cusforacc.bank == Bank.bankId', backref='cusforaccs')
    customer = db.relationship('Customer', primaryjoin='Cusforacc.cusID == Customer.cusID', backref='cusforaccs')


t_cusforloan = db.Table(
    'cusforloan',
    db.Column('loanID', db.ForeignKey('loan.loanID', ondelete='CASCADE'), primary_key=True, nullable=False),
    db.Column('cusID', db.ForeignKey('customer.cusID'), primary_key=True, nullable=False, index=True)
)


class Customer(db.Model):
    __tablename__ = 'customer'

    cusID = db.Column(db.Integer(), primary_key=True)
    cusname = db.Column(db.String(10), nullable=False)
    cusphone = db.Column(db.String(11), nullable=False)
    address = db.Column(db.String(50))
    contact_phone = db.Column(db.String(11), nullable=False)
    contact_name = db.Column(db.String(10), nullable=False)
    contact_Email = db.Column(db.String(20))
    relation = db.Column(db.String(10), nullable=False)
    loanres = db.Column(db.ForeignKey('employee.empID'), index=True)
    accres = db.Column(db.ForeignKey('employee.empID'), index=True)
    employee_id = db.Column(db.ForeignKey('employee.empID'))
    bank_id = db.Column(db.ForeignKey('bank.bankId'))
    create_time = db.Column(db.DateTime, default=datetime.now)

    employee = db.relationship('Employee', primaryjoin='Customer.employee_id == Employee.empID',
                               backref='employee_customers')
    employee1 = db.relationship('Employee', primaryjoin='Customer.loanres == Employee.empID',
                                backref='employee_customers_0')
    loan = db.relationship('Loan', secondary='cusforloan', backref='customers')


class Department(db.Model):
    __tablename__ = 'department'

    departID = db.Column(db.Integer(), primary_key=True)
    departname = db.Column(db.String(20), nullable=False)
    departtype = db.Column(db.String(15))
    manager = db.Column(db.String(18), nullable=False)
    bank = db.Column(db.ForeignKey('bank.bankId'), nullable=False, index=True)

    bank1 = db.relationship('Bank', primaryjoin='Department.bank == Bank.bankId', backref='departments')


class Employee(db.Model):
    __tablename__ = 'employee'
    __table_args__ = (
        db.CheckConstraint("(`emptype` in (_utf8mb4'0',_utf8mb4'1'))"),
    )

    empID = db.Column(db.Integer(), primary_key=True)
    empname = db.Column(db.String(20), nullable=False)
    empphone = db.Column(db.String(11))
    empaddr = db.Column(db.String(50))
    emptype = db.Column(db.String(1))
    empstart = db.Column(db.DateTime(), nullable=False)
    depart = db.Column(db.ForeignKey('department.departID'), index=True)
    password = db.Column(db.String(100))
    bank_id = db.Column(db.ForeignKey('bank.bankId', ondelete='CASCADE'), nullable=True)

    bank = db.relationship('Bank', primaryjoin='Bank.bankId == Employee.bank_id', backref='bank')

    department = db.relationship('Department', primaryjoin='Employee.depart == Department.departID',
                                 backref='employees')


class Loan(db.Model):
    __tablename__ = 'loan'

    loanID = db.Column(db.Integer(), primary_key=True)
    money = db.Column(db.Float(asdecimal=True))
    bank = db.Column(db.ForeignKey('bank.bankId'), index=True)
    state = db.Column(db.String(1), default=0)  # 0未放款， 1 放款中，2 放款完成
    create_time = db.Column(db.DateTime, default=datetime.now)

    bank1 = db.relationship('Bank', primaryjoin='Loan.bank == Bank.bankId', backref='loans')
    customer_id = db.Column(db.ForeignKey('customer.cusID'))
    customer = db.relationship('Customer', primaryjoin='Loan.customer_id == Customer.cusID', backref='loans')

    @classmethod
    def get_loan_by_cusID(cls, cusID, bankId):
        return cls.query.filter_by(customer_id=cusID, bank=bankId).first()

    @classmethod
    def get_loan_by_bankId(cls, bankId):
        return cls.query.filter_by(bank=bankId).all()


class Payinfo(db.Model):
    __tablename__ = 'payinfo'

    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    loanID = db.Column(db.ForeignKey('loan.loanID', ondelete='CASCADE'), nullable=False)
    cusID = db.Column(db.ForeignKey('customer.cusID'), nullable=False, index=True)
    money = db.Column(db.Float(asdecimal=True), nullable=False)
    paytime = db.Column(db.DateTime, nullable=False)

    customer = db.relationship('Customer', primaryjoin='Payinfo.cusID == Customer.cusID', backref='payinfos')
    loan = db.relationship('Loan', primaryjoin='Payinfo.loanID == Loan.loanID', backref='payinfos')
