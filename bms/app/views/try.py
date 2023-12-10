from flask import render_template, request, session

from app.models import Customer, db, Loan, Employee, Bank, Payinfo

cusname = request.args.get('cusname', None)
q = []
if cusname:
    q.append(Customer.cusname.like('%{}%'.format(cusname)))
print(q)
