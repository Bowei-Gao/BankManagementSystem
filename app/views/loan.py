from datetime import datetime

from flask import Blueprint, jsonify
from flask import render_template, request, session

from app.models import Customer, db, Loan, Employee, Bank, Payinfo

bp = Blueprint('loan', __name__)


@bp.route('/loan')
def loan():
    """
    所有贷款页面
    :return:
    """
    return render_template('all_loan.html')


@bp.route('/all_loan')
def all_loan():
    """
    所有贷款数据
    :return:
    """
    cusname = request.args.get('cusname', None)
    # 有查询条件
    q = []
    if cusname:
        q.append(Customer.cusname.like('%{}%'.format(cusname)))
    empID = session.get('empID')
    emp_info = Employee.query.get(empID)
    bank = emp_info.bank
    q.append(Loan.bank == bank.bankId)
    all_loan_list = Loan.query.filter(*q).order_by(Loan.create_time.desc()).all()
    count = len(all_loan_list)
    resp = list()
    for loan in all_loan_list:
        to_lend_money = 0
        pay_info = Payinfo.query.filter_by(loanID=loan.loanID).all()
        if pay_info:
            for pay in pay_info:
                to_lend_money += pay.money
        loan_dict = dict()
        loan_dict['money'] = float(loan.money)
        loan_dict['state'] = loan.state
        loan_dict['loanID'] = loan.loanID
        loan_dict['bank'] = loan.bank1.bankname
        loan_dict['customer'] = loan.customer.cusname
        loan_dict['to_lend_money'] = float(to_lend_money)
        loan_dict['create_time'] = loan.create_time.strftime('%Y-%m-%d %H:%M:%S')
        resp.append(loan_dict)
    print(resp)
    result = {
        "msg": "success",
        "code": "0",
        "count": count,
        "data": resp
    }
    print(result)
    return jsonify(result)


@bp.route('/add_loan', methods=['GET', 'POST'])
def add_loan():
    """
    新增贷款
    :return:
    """
    if request.method == 'GET':
        empID = session.get('empID')
        emp_info = Employee.query.get(empID)
        bank = emp_info.bank
        already_loaned_list = Loan.get_loan_by_bankId(bank.bankId)
        already_loaned_count = 0
        if already_loaned_list:
            for loan in already_loaned_list:
                already_loaned_count += loan.money
        # 可用贷款余额
        available = bank.money - already_loaned_count
        customer_info = Customer.query.all()
        return render_template('add_loan.html', bank=bank, emp_info=emp_info, customer_info=customer_info,
                               available=float(available))

    if request.method == 'POST':
        bankId = request.form.get('bankId')
        cusID = request.form.get('cusID')
        money = request.form.get('money', None)
        if money == '0' and money is None:
            return jsonify({'code': -1, 'msg': '请输入贷款额度！'})
        # 查询当前账户有没有贷款
        loan_info = Loan.get_loan_by_cusID(cusID, bankId)
        # 银行信息
        bank_info = Bank.query.get(bankId)
        # 查询当前银行所有贷款信息， 以贷款的总额
        already_loaned_list = Loan.get_loan_by_bankId(bankId)
        already_loaned_count = 0
        if already_loaned_list:
            for loan in already_loaned_list:
                already_loaned_count += loan.money
        # 可用贷款余额
        available = bank_info.money - already_loaned_count
        # 如果有的话，判断贷款是否完成
        if float(money) > available:
            return jsonify({'code': -1, 'msg': '当前申请贷款额度大于银行可贷款额度！'})
        if loan_info:
            if loan_info.state != '2':
                return jsonify({'code': -1, 'msg': '当前账户有未完成的贷款！'})
            else:
                try:
                    loan_info = Loan()
                    loan_info.customer_id = cusID
                    loan_info.bank = bankId
                    loan_info.money = money
                    db.session.add(loan_info)
                    db.session.commit()
                except Exception as err:
                    return jsonify({'code': -1, 'msg': '新增贷款失败！'})
                return jsonify({'code': 0, 'msg': '新增贷款成功！'})
        try:
            loan_info = Loan()
            loan_info.customer_id = cusID
            loan_info.bank = bankId
            loan_info.money = money
            db.session.add(loan_info)
            db.session.commit()
        except Exception as err:
            return jsonify({'code': -1, 'msg': '新增贷款失败！'})
        return jsonify({'code': 0, 'msg': '新增贷款成功！'})


@bp.route('/make_loans/<int:loanID>', methods=['GET', 'POST'])
def make_loans(loanID):
    emp_info = Employee.query.get(session.get('empID'))
    bank = emp_info.bank
    loan_info = Loan.query.get(loanID)
    customer = loan_info.customer
    to_lend_money = 0
    pay_info = Payinfo.query.filter_by(loanID=loanID).all()
    if pay_info:
        for pay in pay_info:
            to_lend_money += pay.money
    if request.method == 'GET':
        return render_template('make_loans.html', bank=bank, loan_info=loan_info,
                               customer=customer, to_lend_money=to_lend_money)
    if request.method == 'POST':
        money = request.form.get('money')
        cusID = request.form.get('cusID')
        paytime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if loan_info.state == '2':
            return jsonify({'code': -1, 'msg': '贷款以全额发放！'})
        if float(to_lend_money) + float(money) > float(loan_info.money):
            return jsonify({'code': -1, 'msg': '当前放款额度超过最大贷款额度！'})
        try:
            # 新增返款信息
            p_info = Payinfo()
            p_info.money = money
            p_info.loanID = loanID
            p_info.cusID = cusID
            p_info.paytime = paytime
            # 返款后修改放款状态
            if float(to_lend_money) + float(money) == float(loan_info.money):
                loan_info.state = '2'
            else:
                loan_info.state = '1'
            db.session.add(p_info, loan_info)
            db.session.commit()
        except Exception as err:
            print(err)
            return jsonify({'code': -1, 'msg': '操作失败！'})
        return jsonify({'code': 0, 'msg': '放款成功！'})


@bp.route('/del_loan/<int:loanID>', methods=['POST'])
def del_loan(loanID):
    """
    删除贷款
    :param loanID:
    :return:
    """
    if request.method == 'POST':
        try:
            loan_info = Loan.query.get(loanID)
            p_info = Payinfo.query.filter_by(loanID=loanID).all()
            db.session.delete(loan_info)
            [db.session.delete(p) for p in p_info]
            db.session.commit()
        except Exception as err:
            print(err)
            return jsonify({'code': -1, 'msg': '操作失败！'})
        return jsonify({'code': 0, 'msg': '删除成功！'})
