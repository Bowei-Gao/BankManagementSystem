from marshmallow import Schema, fields


class CustomerSchema(Schema):
    cusID = fields.Int()
    cusname = fields.Str()
    cusphone = fields.Str()
    address = fields.Str()
    contact_phone = fields.Str()
    contact_name = fields.Str()
    contact_Email = fields.Str()
    relation = fields.Str()
    account = fields.Nested('AccountSchema')


class AccountSchema(Schema):
    accountID = fields.Int()
    money = fields.Float()
    settime = fields.Str()
    accounttype = fields.Str()
    accountNumber = fields.Str()
    bank = fields.Nested('BankSchema')
    customer = fields.Nested('CustomerSchema')


class BankSchema(Schema):
    bankId = fields.Int()
    bankname = fields.Str()
    city = fields.Str()
    money = fields.Str()


class EmployeeSchema(Schema):
    empID = fields.Int()
    empname = fields.Str()
    empphone = fields.Str()
    empaddr = fields.Str()


class LoanSchema(Schema):
    loanID = fields.Int()
    money = fields.Float()
    bank = fields.Str()
    bank1 = fields.Nested('BankSchema')
    state = fields.Str()
    accounts_id = fields.Str()
    accounts = fields.Nested('AccountSchema')
