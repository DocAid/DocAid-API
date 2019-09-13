from flask import Flask, redirect, url_for,request,jsonify
from firebase_admin import credentials, firestore, initialize_app
app = Flask(__name__)



cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')

patient_details = db.collection('patient_details')


# Api1: Patient_details: POST_REQUEST
@app.route('/patient_details_post',methods=['POST'])
def patient_details_post():
    requestData = request.json
    pid = requestData['pid']
    res = patient_details.document(pid).set(request.json)
    data = {
        "message":"patient_added",
        "pid": pid 
    }
    return data


# Api1: Patient_details_get : GET Request
@app.route('/patient_details_get',methods=['GET'])
def patient_details_get():
    Requestdata = request.json
    pid = Requestdata['pid']
    data = patient_details.document(pid).get()
    return jsonify(data.to_dict())


if __name__ == '__main__':
   app.run(debug = True)
