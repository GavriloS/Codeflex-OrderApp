import pdfkit
from flask import make_response

from model.stack import Stack


# creates pdf file from html
def createPdf(html):
    # if it doesnt work download khtmltopdf from link https://wkhtmltopdf.org/downloads.html and edit the path correctly
    config = pdfkit.configuration(wkhtmltopdf="C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe")
    pdf = pdfkit.from_string(html, False, configuration=config)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"

    return response


# calculates toatl price of an order
def calculateOrderPrice(order):
    price = 0
    for item in order:
        price += float(item["unit_price"]) * float(item["quantity_in_box"])
    return round(price, 2)

# stacks the items for an order
def stackItemsFromOrder(order):
    stacks = []
    stacks.append(Stack([], 0))
    while True:
        maxWeight = 0
        maxWeightItem = None
        # find item with highest max capacity
        for item in order:
            if (maxWeight <= int(item["max_weight_capacity"])):
                maxWeightItem = item
                maxWeight = int(item["max_weight_capacity"])

        if (maxWeightItem == None):
            break
        # remove the item from the inital order
        order.remove(maxWeightItem)
        #check if stacks are empty and puts the first element
        if (len(stacks[0].items) == 0):
            stacks[0].items.append(maxWeightItem)
            continue

        inStack = False

        for i in range(len(stacks)):
            putInStack = True
            #checks if item can be put in one of the existing stacks
            for item in stacks[i].items:
                tempCurrentweight = stacks[i].currentWeight + maxWeightItem["weight"] * maxWeightItem["quantity_in_box"]
                if (tempCurrentweight > item["max_weight_capacity"]):
                    putInStack = False
                    break
            #puts item in existing stack
            if (putInStack):
                stacks[i].items.append(maxWeightItem)
                stacks[i].currentWeight += maxWeightItem["weight"] * maxWeightItem["quantity_in_box"]
                inStack = True
                break
        # if item cant be put in any of the stacks a new stack is created
        if (inStack == False):
            stacks.append(Stack([], 0))
            stacks[-1].items.append(maxWeightItem)
    return stacks

# gets the tax ammount for one item
def getTax(item):
    price = item["unit_price"]
    if (item["tax_type"] == "high"):
        price = (price * 100) / 121
    elif (item["tax_type"] == "low"):
        price = (price * 100) / 107
    tax = item["unit_price"] - round(price, 2)
    return round(tax, 2)

# gets the total tax ammount from an order
def getTotalTax(order):
    totalTax = 0
    for item in order:
        totalTax += getTax(item)
    return totalTax

# get the customer by Id from list
def getCustomerById(customers, id):
    customer = None
    for c in customers:
        if int(c["id"]) == int(id):
            customer = c
            break
    return customer

# gets the customer order by the orderNumber from list
def getCustomerOrderByOrderNumber(customerOrders,orderNum):
    customerOrder = None
    for co in customerOrders:
        if str(co["order_no"]) == str(orderNum):
            customerOrder = co
            break
    return customerOrder