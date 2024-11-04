from flask import Flask, jsonify, request
import uuid
import random
import requests
import os

orders = []

def getOrders():
    return orders

def createOrder(amount=1):
    orderlines = []
    for x in range(amount):
        new_order = {
            'id': uuid.uuid4().hex,
            'productId': random.randint(1000000000,9999999999),
            'amount': random.randint(0,10),
            'completed': False
        }
        orderlines.append(new_order)
        
    new_order = {
        'id': uuid.uuid4().hex,
        'orderlines': orderlines,
        'readyForPickup': False,
        'completed': False
    }
    orders.append(new_order)
    return new_order
    
def getOrder(orderId):
    order = [order for order in orders if order['id'] == orderId]
    if len(order) == 0:
        return []
    return order[0]

def updateOrder(orderId,complete=False):
    order = [order for order in orders if order['id'] == orderId]
    if len(order) == 0:
        return []
    order[0]['completed'] = complete
    return order

def updateOrderLine(orderId,lineId,complete=False):
    order = [order for order in orders if order['id'] == orderId]
    if len(order) == 0:
        return []
    orderLine = [line for line in order[0]['orderlines'] if line['id'] == lineId]
    orderLine[0]['completed'] = complete
    incompleteLines = [line for line in order[0]['orderlines'] if line['completed'] == False]
    if len(incompleteLines) == 0:
        order[0]['readyForPickup'] = True
        print("SEND EMAIL")
    return orderLine