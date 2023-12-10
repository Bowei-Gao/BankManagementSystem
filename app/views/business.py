from flask import Blueprint, request, render_template, session
from app.models import Account, Employee, Customer, Loan
from utils.common import *

bp = Blueprint('business', __name__)


@bp.route('/business', methods=['GET'])
def business():
    """
    业务统计
    :return:
    """
    emp_info = Employee.query.get(session.get('empID'))
    bank_id = emp_info.bank_id
    bankname = emp_info.bank.bankname

    dimension = request.args.get('dimension', None)
    if dimension == 'quarter':
        data = ['第一季度', '第二季度', '第三季度', '第四季度']
        customer_quarter_list = []
        # 储蓄账户
        storage_quarter_list = []
        # 支票账户
        check_quarter_list = []
        # 储蓄账户总额
        storage_quarter_money_lis = []
        # 贷款总额
        check_quarter_money_lis = []
        for i in range(1, 5):
            start, end = get_quarter(i)
            customer_quarter_count = Customer.query.filter(Customer.create_time >= start).filter(
                Customer.create_time <= end, Customer.bank_id == bank_id).count()
            customer_quarter_list.append(customer_quarter_count)
            storage_quarter_count = Account.query.filter(Account.settime >= start,
                                                         Account.accounttype == '储蓄账户',
                                                         Account.bank_id == bank_id).filter(
                Account.settime <= end).count()
            storage_quarter_list.append(storage_quarter_count)
            check_quarter_count = Account.query.filter(Account.settime >= start, Account.accounttype == '支票账户',
                                                       Account.bank_id == bank_id).filter(
                Account.settime <= end).count()
            check_quarter_list.append(check_quarter_count)
            # 存储账户总额统计
            storage_quarter_money = Account.query.filter(Account.settime >= start,
                                                         Account.accounttype == '储蓄账户',
                                                         Account.bank_id == bank_id).filter(
                Account.settime <= end).all()
            storage_money = 0
            if storage_quarter_money:
                for storage in storage_quarter_money:
                    storage_money += float(storage.money)
            storage_quarter_money_lis.append(storage_money / 10000)

            # 贷款总额统计
            check_quarter_money = Loan.query.filter(Loan.create_time >= start, Loan.bank == bank_id).filter(
                Account.settime <= end).all()
            check_money = 0
            if check_quarter_money:
                for check in check_quarter_money:
                    check_money += float(check.money)
            check_quarter_money_lis.append(check_money / 10000)
        return render_template('business_statistics.html',
                               customer_list=customer_quarter_list,
                               data=data,
                               bankname=bankname,
                               dimension=dimension,
                               storage_list=storage_quarter_list,
                               check_list=check_quarter_list,
                               storage_money_lis=storage_quarter_money_lis,
                               check_money_lis=check_quarter_money_lis,
                               )
    elif dimension == 'year':
        data = []
        customer_year_list = []
        # 储蓄账户
        storage_year_list = []
        # 支票账户
        check_year_list = []
        # 储蓄账户总额
        storage_year_money_lis = []
        # 贷款总额
        check_year_money_lis = []
        for i in range(0, 5):
            start, end, date = get_year(i)
            data.append(date)
            customer_month_count = Customer.query.filter(Customer.create_time >= start).filter(
                Customer.create_time <= end, Customer.bank_id == bank_id).count()
            customer_year_list.append(customer_month_count)
            # 储蓄账户
            storage_year_count = Account.query.filter(Account.settime >= start, Account.accounttype == '储蓄账户',
                                                      Account.bank_id == bank_id).filter(
                Account.settime <= end).count()
            storage_year_list.append(storage_year_count)
            # 支票账户
            check_year_count = Account.query.filter(Account.settime >= start, Account.accounttype == '支票账户',
                                                    Account.bank_id == bank_id).filter(
                Account.settime <= end).count()
            check_year_list.append(check_year_count)
            # 存储账户总额统计
            storage_year_money = Account.query.filter(Account.settime >= start, Account.accounttype == '储蓄账户',
                                                      Account.bank_id == bank_id).filter(
                Account.settime <= end).all()
            storage_money = 0
            if storage_year_money:
                for storage in storage_year_money:
                    storage_money += float(storage.money)
            storage_year_money_lis.append(storage_money / 10000)

            # 贷款总额统计

            check_year_money = Loan.query.filter(Loan.create_time >= start, Loan.bank == bank_id).filter(
                Loan.create_time <= end).all()
            check_money = 0
            if check_year_money:
                for check in check_year_money:
                    check_money += float(check.money)
            check_year_money_lis.append(check_money / 10000)
        return render_template('business_statistics.html',
                               dimension=dimension,
                               data=list(reversed(data)),
                               bankname=bankname,
                               customer_list=list(reversed(customer_year_list)),
                               storage_list=list(reversed(storage_year_list)),
                               check_list=list(reversed(check_year_list)),
                               storage_money_lis=list(reversed(storage_year_money_lis)),
                               check_money_lis=list(reversed(check_year_money_lis)),
                               )
    else:
        data = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        dimension = 'month'
        customer_month_list = []
        # 储蓄账户
        storage_month_list = []
        # 支票账户
        check_month_list = []
        # 储蓄账户总额
        storage_month_money_lis = []
        # 贷款总额
        check_month_money_lis = []
        for i in range(1, 13):
            start, end = get_month(i)
            customer_month_count = Customer.query.filter(Customer.create_time >= start).filter(
                Customer.create_time <= end, Customer.bank_id == bank_id).count()
            customer_month_list.append(customer_month_count)
            # 储蓄账户
            storage_month_count = Account.query.filter(Account.settime >= start, Account.accounttype == '储蓄账户',
                                                       Account.bank_id == bank_id).filter(
                Account.settime <= end).count()
            storage_month_list.append(storage_month_count)
            # 支票账户
            check_month_count = Account.query.filter(Account.settime >= start, Account.accounttype == '支票账户',
                                                     Account.bank_id == bank_id).filter(
                Account.settime <= end).count()
            check_month_list.append(check_month_count)
            # 存储账户总额统计
            storage_month_money = Account.query.filter(Account.settime >= start, Account.accounttype == '储蓄账户',
                                                       Account.bank_id == bank_id).filter(
                Account.settime <= end).all()
            storage_money = 0
            if storage_month_money:
                for storage in storage_month_money:
                    storage_money += float(storage.money / 10000)  # 万元为单位计算
            storage_month_money_lis.append(storage_money)

            # 贷款总额统计
            check_month_money = Loan.query.filter(Loan.create_time >= start, Loan.bank == bank_id).filter(
                Account.settime <= end).all()
            check_money = 0
            if check_month_money:
                for check in check_month_money:
                    check_money += float(check.money)
            check_month_money_lis.append(check_money / 10000)

        return render_template('business_statistics.html',
                               customer_list=customer_month_list,
                               data=data,
                               bankname=bankname,
                               dimension=dimension,
                               storage_list=storage_month_list,
                               check_list=check_month_list,
                               storage_money_lis=storage_month_money_lis,
                               check_money_lis=check_month_money_lis,
                               )

