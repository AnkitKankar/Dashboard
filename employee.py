from flask import Flask,request,jsonify
from pymongo import MongoClient
import pymongo
import ssl

app = Flask(__name__)


CONNECTION_STRING ="mongodb+srv://admin:admin@cluster0.wm8q8.mongodb.net/covid_tracker"
# ?retryWrites=true&w=majority
client = MongoClient(CONNECTION_STRING)

# Create the database for our example (we will use the same database throughout the tutorial
db = client['company_dashboard']


ssl._create_default_https_context = ssl._create_unverified_context

@app.route('/registerEmployee',methods=['POST']) 
def RegisterUser():
    req = request.json
    try:
        employee_data = [int(x['employeeId']) for x in db.employee_data.find({},{'employeeId':1})]
        employee_id = str(max(employee_data)+1)
        req['employeeId'] = user_id
        db.employee_data.insert_one(req)
        return  jsonify({'employeeId':employee_id})
    
    except Exception as e:
        return jsonify({
            "message":str(e),
            "Status":"Failure"
        }) 

@app.route('/removeEmployee',methods=['POST'])
def RemoveUser():
    req = request.json
    try:
        employee_data = db.employee_data.find_one({
            "employeeId":req['employeeId']
        },{"_id":0})

        if employee_data:
            db.employee_data.delete_one({"employeeId":req['employeeId']})
            return jsonify({
                "message":"Employee Deleted Successfully"
            })
    except Exception as e:
        return jsonify({
            "message":str(e),
            "Status":"Failure"
        })

@app.route('/updateEmployee',methods=['POST'])
def UpdateUser():
    req = request.json
    try:
        employee_data = db.employee_data.find_one({
            "employeeId":req['employeeId']
        },{"_id":0})
        if employee_data:
            db.employee_data.update_one({
                "employeeId":req['employeeid']
            },{"$set":req})
        return jsonify({
                "message":"Employee updated Successfully"
            })
    except Exception as e:
        return jsonify({
            "message":str(e),
            "Status":"Failure"
        })
app.run(host='localhost', port=81)