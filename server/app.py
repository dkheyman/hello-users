
import json
import logging
import os
import time
from datetime import date, datetime
from flask import Flask, jsonify, request

import boto3

app = Flask(__name__)

IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
else:
    dynamodb = boto3.resource('dynamodb')

@app.route("/")
def default():
    return jsonify("Hello World")

@app.route("/hello", methods=["GET"])
def list():
    table = dynamodb.Table("usersTable")

    result = table.scan(
        AttributesToGet=["username"]
    )
    response = {
        "body": result["Items"]
    }

    return jsonify(response), 200
    

@app.route("/hello/<string:username>", methods=["GET"])
def get(username):
    table = dynamodb.Table("usersTable")

    result = table.get_item(
        Key={
            'username': username
        }
    )

    if "Item" in result:
        item = result['Item']
    else:
        return jsonify({
        "message": "No such username %s exists" % username
    }), 404

    today_date = date.today()
    birthday = item.get('dateOfBirth')
    bday_struct = time.strptime(birthday, "%Y-%m-%d")
    birthday_date = date(today_date.year, bday_struct.tm_mon, bday_struct.tm_mday)
    days_left = (birthday_date - today_date).days
    if days_left == 0:
        message = "Hello %s! Happy Birthday!" % username 
    elif days_left > 0:
        message = "Hello %s! your birthday is in %s days." % (username, days_left)
    else:
        next_year_bday = date(today_date.year+1, bday_struct.tm_mon, bday_struct.tm_mday)
        days_left = (next_year_bday - today_date).days
        message = "Hello %s! your birthday is in %s days." % (username, days_left)

    response = {
        "message": message
    }

    return jsonify(response), 200

@app.route("/hello/<string:username>", methods=["PUT"])
def put(username):
    data = request.json.get('dateOfBirth', '')
    if not username.isalpha():
        return jsonify({
            "message": "username must be alphabetic"
    }), 400

    try:
        date_struct = time.strptime(data, '%Y-%m-%d')
        today = date.today()
        assert(date(date_struct.tm_year, date_struct.tm_mon, date_struct.tm_mday) <= today)
    except ValueError as e:
        return jsonify({
            "message": "dateOfBirth must be in format YYYY-mm-dd"
    }), 400
    except AssertionError as e:
        return jsonify({
            "message": "dateOfBirth must be earlier than present day"
    }), 400

    try:
        table = dynamodb.Table('usersTable')

        result = table.update_item(
            Key={
                'username': username
            },
            ExpressionAttributeValues={
                ':dateOfBirth': data,
            },
            UpdateExpression='SET dateOfBirth = :dateOfBirth',
            ReturnValues='ALL_NEW'
        )
    except Exception as e:
        return jsonify({
            "message": str(e)
    }), 500

    if result['ResponseMetadata']['HTTPStatusCode'] > 300:
        return jsonify({
        "message": "Unable to update item"
    }), result['ResponseMetadata']['HTTPStatusCode']
    else:
        return '', result['ResponseMetadata']['HTTPStatusCode']
