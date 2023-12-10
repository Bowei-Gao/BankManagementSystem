from flask import Blueprint, jsonify, session
from flask import render_template, request

from app.models import Customer, db, Employee, Account
from app.forms.serializes import CustomerSchema
from app.views.employee import login_check

bp = Blueprint('customer', __name__)


@bp.route('/')
@login_check
def hello_world():
    return render_template('base.html')


@bp.route('/customer')
def customer():
    """
    所有客户页面
    :return:
    """
    return render_template('all_customer.html')


@bp.route('/all_customer')
def all_customer():
    """
    所有客户数据返回
    :return:
    """
    cusname = request.args.get('cusname', None)
    emp_info = Employee.query.get(session.get('empID'))
    bank_id = emp_info.bank_id
    # 有查询条件
    q = []
    if cusname:
        q.append(Customer.cusname.like('%{}%'.format(cusname)))
    all_customer_list = Customer.query.filter(*q, Customer.bank_id == bank_id).order_by(Customer.cusID.desc()).all()
    count = len(all_customer_list)
    resp = CustomerSchema().dump(all_customer_list, many=True)
    print(resp)
    result = {
        "msg": "success",
        "code": "0",
        "count": count,
        "data": resp
    }
    return jsonify(result)


@bp.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    """
    添加客户
    :return:
    """
    if request.method == 'POST':
        print(request.form)
        cusname = request.form.get('cusname')
        cusphone = request.form.get('cusphone')
        relation = request.form.get('relation')
        contact_name = request.form.get('contact_name')
        contact_phone = request.form.get('contact_phone')
        address = request.form.get('address')
        contact_Email = request.form.get('contact_Email')
        empID = session.get('empID')
        emp_info = Employee.query.get(empID)
        bank_id = emp_info.bank_id
        try:
            customer_info = Customer()
            customer_info.cusname = cusname
            customer_info.cusphone = cusphone
            customer_info.relation = relation
            customer_info.contact_name = contact_name
            customer_info.contact_phone = contact_phone
            customer_info.address = address
            customer_info.contact_Email = contact_Email
            customer_info.bank_id = bank_id
            customer_info.employee_id = empID
            db.session.add(customer_info)
            db.session.commit()
        except Exception as err:
            print(err)
            return jsonify({'code': -1})
        return jsonify({'code': 0})
    else:
        return render_template('add_customer.html')


@bp.route('/edit_customer', methods=['GET', 'POST'])
def edit_customer():
    """
    更新客户
    :return:
    """
    if request.method == 'POST':
        print(request.form)
        cusID = request.form.get('cusID')
        cusname = request.form.get('cusname')
        cusphone = request.form.get('cusphone')
        relation = request.form.get('relation')
        contact_name = request.form.get('contact_name')
        contact_phone = request.form.get('contact_phone')
        address = request.form.get('address')
        contact_Email = request.form.get('contact_Email')
        try:
            customer_info = Customer.query.get(cusID)
            customer_info.cusname = cusname
            customer_info.cusphone = cusphone
            customer_info.relation = relation
            customer_info.contact_name = contact_name
            customer_info.contact_phone = contact_phone
            customer_info.address = address
            customer_info.contact_Email = contact_Email
            db.session.commit()
        except Exception as err:
            print(err)
            return jsonify({'code': -1})
        return jsonify({'code': 0})
    else:
        cusID = request.args.get('cusID')
        print(cusID)
        customer_info = Customer.query.get(cusID)
        return render_template('edit_customer.html', customer_info=customer_info)


@bp.route('/del_customer', methods=['POST'])
def del_customer():
    """
    删除客户
    :return:
    """
    # todo 校验客户是否有存款
    if request.method == "POST":
        cusID = request.form.get('cusID')
        customer = Customer.query.get(cusID)
        account_info = Account.query.filter_by(customer_id=cusID).all()
        if account_info:
            return jsonify({'code': -1, 'msg': '当前用户还有开户信息！'})
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'code': 0})
