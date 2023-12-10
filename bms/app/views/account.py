from flask import Blueprint, request, render_template, session, redirect, jsonify

from app.forms.serializes import AccountSchema
from app.models import Account, Employee, Customer, Bank, Loan
from app.config import db
from datetime import datetime

bp = Blueprint('account', __name__)


@bp.route('/account')
def account():
    """
    所有账户页面
    :return:
    """
    return render_template('all_account.html')


@bp.route('/all_account')
def all_account():
    """
    所有客户数据返回
    :return:
    """
    emp_info = Employee.query.get(session.get('empID'))
    bank = emp_info.bank
    accountNumber = request.args.get('accountNumber', None)
    # 有查询条件
    q = []
    if accountNumber:
        q.append(Account.accountNumber.like('%{}%'.format(accountNumber)))
    q.append(Account.bank_id == bank.bankId)
    all_account_list = Account.query.filter(*q).order_by(Account.accountID.desc()).all()
    count = len(all_account_list)
    resp = AccountSchema().dump(all_account_list, many=True)
    # 没有查询条件
    result = {
        "msg": "success",
        "code": "0",
        "count": count,
        "data": resp
    }
    return jsonify(result)


@bp.route('/add_account', methods=['GET', 'POST'])
def add_account():
    """
    添加账户
    :return:
    """
    if request.method == 'POST':
        print(request.form)
        accounttype = request.form.get('accounttype')
        money = request.form.get('money')
        accountNumber = request.form.get('accountNumber')
        bankId = request.form.get('bankId')
        empID = request.form.get('empID')
        cusID = request.form.get('cusID')
        # 校验有没有账号
        account_info = Account.query.filter_by(accountNumber=accountNumber).all()
        if account_info:
            return jsonify({'code': -1, 'msg': '当前账号已存在！'})
        all_customer_account_type = Account.query.filter_by(customer_id=cusID, bank_id=bankId).all()
        if all_customer_account_type:
            for account_type in all_customer_account_type:
                if account_type.accounttype == accounttype:
                    return jsonify({'code': -1, 'msg': '当前开户人已有[{}]卡！'.format(accounttype)})
            try:
                account_info = Account()
                account_info.accounttype = accounttype
                account_info.bank_id = bankId
                account_info.employee_id = empID
                account_info.customer_id = cusID
                account_info.money = money
                account_info.accountNumber = accountNumber
                account_info.settime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                db.session.add(account_info)
                db.session.commit()
            except Exception as err:
                print(err)
                return jsonify({'code': -1})
            return jsonify({'code': 0})

        else:
            try:
                account_info = Account()
                account_info.accounttype = accounttype
                account_info.bank_id = bankId
                account_info.employee_id = empID
                account_info.customer_id = cusID
                account_info.money = money
                account_info.accountNumber = accountNumber
                account_info.settime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                db.session.add(account_info)
                db.session.commit()
            except Exception as err:
                print(err)
                return jsonify({'code': -1})
            return jsonify({'code': 0})

    else:
        empID = session.get('empID')
        # 员工信息
        emp_info = Employee.query.get(empID)
        # 银行信息
        bank = emp_info.bank
        # 开户人
        customer = Customer.query.filter(Customer.bank_id == bank.bankId)
        return render_template('add_account.html', bank=bank, emp_info=emp_info, customer=customer)


@bp.route('/edit_account/<int:accountID>', methods=['GET', 'POST'])
def edit_account(accountID):
    """
    编辑账户
    :param accountID:
    :return:
    """
    # post请求提交修改
    if request.method == 'POST':
        print(request.form)
        accounttype = request.form.get('accounttype')
        money = request.form.get('money')
        bankId = request.form.get('bankId')
        cusID = request.form.get('cusID')
        try:
            account_info = Account.query.get(accountID)
            account_info.accounttype = accounttype
            account_info.bank_id = bankId
            account_info.customer_id = cusID
            account_info.money = money
            db.session.add(account_info)
            db.session.commit()
        except Exception as err:
            print(err)
            return jsonify({'code': -1, 'msg': '修改失败！'})
        return jsonify({'code': 0})
    # get获取详情
    if request.method == 'GET':
        account_info = Account.query.get(accountID)
        bank = account_info.bank
        customer = Customer.query.all()
        return render_template('edit_account.html', account_info=account_info, bank=bank, customer=customer)


@bp.route('/del_account/<int:accountID>', methods=['GET', 'POST'])
def del_account(accountID):
    """
    删除
    :param accountID:
    :return:
    """
    # todo 删除校验，是否有存款
    account_info = Account.query.get(accountID)
    db.session.delete(account_info)
    db.session.commit()
    return jsonify({'code': 0})
