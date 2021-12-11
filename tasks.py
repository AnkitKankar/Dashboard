from flask import Flask, request, jsonify
from pymongo import MongoClient
import pymongo
import ssl
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


CONNECTION_STRING = "mongodb+srv://admin:admin123@cluster0.wm8q8.mongodb.net/company_dashboard"
# ?retryWrites=true&w=majority
client = MongoClient(CONNECTION_STRING)

# Create the database for our example (we will use the same database throughout the tutorial
db = client['company_dashboard']


ssl._create_default_https_context = ssl._create_unverified_context


@app.route('/createTask', methods=['POST'])
def CreateTask():
    req = request.json
    try:
        task_data = [int(x['taskId'])
                     for x in db.task_data.find({}, {'taskId': 1})]
        task_id = str(max(task_data)+1)
        req['taskId'] = task_id
        db.task_data.insert_one(req)
        return jsonify({
            "message": "Task Created Successfully"})

    except Exception as e:
        return jsonify({
            "message": str(e),
            "Status": "Failure"
        })


@app.route('/assignTask', methods=['POST'])
def AssignTask():
    req = request.json
    try:
        task_data = db.task_data.find_one({
            "taskId": req['taskId']
        }, {"_id": 0})
        if task_data:
            db.task_data.update_one({
                "taskId": req['taskId']
            }, {"$set": req})
        return jsonify({
            "message": "Task Assigned Successfully"
        })
    except Exception as e:
        return jsonify({
            "message": str(e),
            "Status": "Failure"
        })


@app.route('/taskCompleted', methods=['POST'])
def TaskCompleted():
    req = request.json
    try:
        task_data = db.task_data.find_one({
            "taskId": req['taskId']
        }, {"_id": 0})
        if task_data:
            today_date = datetime.datetime.now().replace(microsecond=0).isoformat()
            req['completedDate'] = today_date
            db.task_data.update_one({
                "taskId": req['taskId']
            }, {"$set": req})
        return jsonify({
            "message": "Task Completed"
        })
    except Exception as e:
        return jsonify({
            "message": str(e),
            "Status": "Failure"
        })


@app.route('/viewAllTasks', methods=["GET"])
def GetAllTask():
    try:
        task_data = [data for data in db.task_data.find({}, {"_id": 0})]
        return jsonify({
            "taskData": task_data
        })
    except Exception as e:
        return jsonify({
            "message": str(e),
            "Status": "Failure"
        })


@app.route('/viewTaskByEmployee', methods=["POST"])
def GetTaskByEmployee():
    req = request.json
    try:
        task_data = [data for data in db.task_data.find(
            {"employeeId": req['employeeId']}, {"_id": 0})]
        return jsonify({
            "taskDataByEmployee": task_data
        })
    except Exception as e:
        return jsonify({
            "message": str(e),
            "Status": "Failure"
        })


@app.route('/findTaskByDate', methods=["POST"])
def FindTaskByDate():
    req = request.json
    try:
        task_by_date = [data for data in db.task_data.find({
            "completedDate": req["completedDate"]
        }, {"_id": 0})]
        return jsonify({
            "taskByDate": task_by_date
        })
    except Exception as e:
        return jsonify({
            "message": str(e),
            "Status": "Failure"
        })


app.run(host='localhost', port=82)
