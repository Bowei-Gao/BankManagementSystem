from flask import Blueprint, request, render_template, session, redirect, jsonify

from app.models import Employee, Account, Customer

bp = Blueprint('employee', __name__)


def login_check(func):
    """
    登录校验
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        if not session.get('empID'):
            return redirect('/login')
        else:
            return func(*args, **kwargs)

    return wrapper


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        empphone = request.form.get('empphone')
        password = request.form.get('password')
        if empphone and password:
            query_list = list()
            query_list.append(Employee.empphone == empphone)
            query_list.append(Employee.password == password)
            employee_info = Employee.query.filter(*query_list).first()
            if employee_info:
                session['empID'] = employee_info.empID
                session['empname'] = employee_info.empname
                return jsonify({'code': 0})
            return jsonify({'code': -1, 'msg': '账号或密码错误！'})
    else:
        return render_template('login.html')


@bp.route('/logout', methods=['GET'])
def logout():
    """
    退出登录
    :return:
    """
    try:
        del session['empID']
        del session['empname']
    except Exception as err:
        return redirect('/login')
    return redirect('/login')


@bp.route('/welcome', methods=['GET'])
def welcome():
    """
    首页
    :return:
    """
    empID = session.get('empID')
    emp_info = Employee.query.get(empID)
    bank = emp_info.bank
    count_account = Account.query.filter_by(bank_id=bank.bankId).count()
    count_customer = Customer.query.filter_by(bank_id=bank.bankId).count()
    return render_template('welcome.html', emp_info=emp_info, bank=bank, count_account=count_account,
                           count_customer=count_customer)
