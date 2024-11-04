from flask import Flask, render_template, request, redirect, url_for
import orders
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def ToDo():
    return render_template(
        "pageNotFound.html"
    )

@app.route('/OrderList')
@app.route('/orderlist')
def OrderList():
    Orders = orders.getOrders()
    allOrders=[]
    for o in Orders:
        allOrders.append((o['id'], o['readyForPickup'], o['completed']))

    return render_template(
        "orderList.html",
        AllOrders=allOrders
    )

@app.route('/OrderDetails')
def OrderDetails():
    orderId = request.args.get('orderId')
    order = orders.getOrder(orderId)
    if len(order) == 0:
        return render_template("error")
    lines=[]
    olines = order['orderlines']
    for oLine in olines:
        lines.append((oLine['productId'], oLine['amount'], oLine['completed'], oLine['id']))

    return render_template(
        "orderDetails.html",
        OrderId = orderId,
        ReadyForPickup = order['readyForPickup'],
        Complete = order['completed'],
        OrderLines=lines
    )

@app.route('/newOrder')
def newOrder():
    lc = request.args.get('lineCount')
    if len(lc) == 0:
        lc = 1
    lineCount = int(lc)
    if lineCount < 1:
        lineCount = 1
    newOrder = orders.createOrder(lineCount)
    if len(newOrder) == 0:
        return render_template("error")
    return redirect(url_for('OrderList'))

@app.route('/readyMaterial')
def readyMaterial():
    orderId = request.args.get('orderId')
    if len(orderId) == 0:
        return render_template("error")
    lineId = request.args.get('lineId')
    if len(lineId) == 0:
        return render_template("error")
    material = orders.updateOrderLine(orderId, lineId, True)
    if len(material) == 0:
        return render_template("error")
    return redirect(url_for('OrderDetails') + "?orderId=" + orderId)

@app.route('/deliverOrder')
def deliverOrder():
    orderId = request.args.get('orderId')
    if len(orderId) == 0:
        return render_template("error")
    order = orders.updateOrder(orderId, True)
    if len(order) == 0:
        return render_template("error")
    return redirect(url_for('OrderDetails') + "?orderId=" + orderId)

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)