import requests
from flask import Flask, render_template
from utils import createPdf, calculateOrderPrice, stackItemsFromOrder, getTax, getTotalTax, getCustomerById, \
    getCustomerOrderByOrderNumber

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET'


# Index route
@app.route("/")
def index():
    url = 'https://assessment.codeflex.it/customers'
    customers = requests.get(url, auth=('user', 'api_user_password1234'))
    customers = customers.json()

    return render_template("index.html", customers=customers)


@app.route("/orders/<customer_id>")
def getCustomerOrders(customer_id: int):
    customerUrl = 'https://assessment.codeflex.it/customers'
    customer = requests.get(customerUrl, auth=('user', 'api_user_password1234'))
    customer = customer.json()

    customer = getCustomerById(customer, customer_id)

    url = 'https://assessment.codeflex.it/customer_orders/' + customer_id
    orders = requests.get(url, auth=('user', 'api_user_password1234'))
    orders = orders.json()
    return render_template('user.html', orders=orders, customer=customer)


@app.route("/invoice/<customer_id>/<order_no>")
def createInvoice(customer_id: int, order_no: str):
    customerUrl = 'https://assessment.codeflex.it/customers'
    customer = requests.get(customerUrl, auth=('user', 'api_user_password1234'))
    customer = customer.json()
    # get the customer from list
    customer = getCustomerById(customer, customer_id)

    orderUrl = "https://assessment.codeflex.it/order_components/" + order_no
    order = requests.get(orderUrl, auth=('user', 'api_user_password1234'))
    order = order.json()

    customerOrderUrl = "https://assessment.codeflex.it/customer_orders/" + customer_id
    customerOrder = requests.get(customerOrderUrl, auth=('user', 'api_user_password1234'))
    print(customerOrder)
    customerOrder = customerOrder.json()

    customerOrder = getCustomerOrderByOrderNumber(customerOrder, order_no)

    html = render_template("invoice.html", getTax=getTax, totalTax=getTotalTax(order),
                           deliveryDate=customerOrder["delivery_date"], customer=customer, order=order,
                           order_no=order_no, totalPrice=calculateOrderPrice(order))
    return createPdf(html)


@app.route("/order-picking/<order_no>")
def orderPicking(order_no: str):
    orderUrl = "https://assessment.codeflex.it/order_components/" + order_no
    order = requests.get(orderUrl, auth=('user', 'api_user_password1234'))
    order = order.json()
    stacks = stackItemsFromOrder(order)
    html = render_template("order-picking.html", stacks=stacks, stackLength=len(stacks))

    return createPdf(html)


if __name__ == "__main__":
    app.run(debug=True)
