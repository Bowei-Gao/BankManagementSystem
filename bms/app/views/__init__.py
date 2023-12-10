from .customer import bp as customer
from .employee import bp as employee
from .account import bp as account
from .loan import bp as loan
from .business import bp as business


def register_app(app):
    app.register_blueprint(customer)
    app.register_blueprint(employee)
    app.register_blueprint(account)
    app.register_blueprint(loan)
    app.register_blueprint(business)
