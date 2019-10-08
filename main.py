
from flask import Flask, redirect, url_for, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import pickle
import json
app = Flask(__name__)
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()

patient_details = db.collection('patient_details')
medicines_diagonized = db.collection('medicines_diagonized')
diagnosis_keywords = db.collection('diagnosis_keywords')

# API SUMMARY

# API1: patient_details_api [POST and GET]
# API2: diagonized_medicines_api [POST GET and PUT]
# API3: diagnosis_keywords_api [POST GET and PUT]


@app.route('/prediction', methods=['POST'])
def prediction():

    requestData = request.json
    print(requestData)
    data = requestData['val']

    if request.method == 'POST':

        model = pickle.load(open('medpred.pickle', 'rb'))
        dummydata = model.predict([data])
        d = str(dummydata[0])
        print(type(d), d)
        with open('medicine.json') as json_file:
            jdata = json.load(json_file)
            # print(jdata)
            data = jdata[d]
        # data = jsonify(dummydata)
        print(data)
        ndata = {d: data}
        jsondata = jsonify(ndata)
        return jsondata


@app.route('/patient_details', methods=['POST', 'GET'])
def patient_details_function():

    requestData = request.json
    pid = requestData['pid']

    if request.method == 'POST':
        data = {
            "message": "patient_added",
            "pid": pid
        }
        return data
    elif request.method == 'GET':
        data = patient_details.document(pid).get()
        return jsonify(data.to_dict())
    else:
        return "Invalid request"


@app.route('/diagonized_medicines', methods=['POST', 'GET', 'PUT'])
def diagonized_medicines():
    requestData = request.json
    pid = requestData['pid']

    if(request.method == 'POST'):
        timestamp = requestData['timestamp']
        medicines_diagonized.document(pid).set(request.json)
        data = {
            "message": "Medicines stored for first time",
            "pid": pid,
            "timestamp": timestamp
        }
        return data

    elif request.method == 'PUT':
        '''
            #Now this is interesting, please note carefully. 
            When the doctor is gonna update it when the user visits second time, 
            Here, the previous json object will be called using get and then the current one will be appended,
            so that it becomes an array of objects according to timestamp. 

            #Thats just json, manipulation, in the api, we will just update the value, whenever a put request is received.
        '''
        # The requestData will obviously change as is sent in the request.
        medicines_diagonized.document(pid).update(requestData)
        data = {
            "message": "Medicines updated",
            "pid": pid,
        }
        return data

    # This will be used while generating the prescription.
    elif(request.method == 'GET'):
        data = medicines_diagonized.document(pid).get()
        return jsonify(data.to_dict())

    else:
        return "Invalid request"


@app.route('/diagnosis_keywords', methods=['GET', 'PUT', 'POST'])
def diagnosis_keywords_function():

    requestData = request.json
    pid = requestData['pid']

    if(request.method == 'POST'):
        timestamp = requestData['timestamp']
        diagnosis_keywords.document(pid).set(request.json)
        data = {
            "message": "Keywords stored!!!",
            "pid": pid,
            "timestamp": timestamp
        }
        return data

    elif request.method == 'PUT':
        '''
            #This is exactly same as the previous API.

            #Now this is interesting, please note carefully. 
            When the doctor is gonna update it when the user visits second time, 
            Here, the previous json object will be called using get and then the current one will be appended,
            so that it becomes an array of objects according to timestamp. 

            #Thats just json, manipulation, in the api, we will just update the value, whenever a put request is received.
        '''
        # The requestData will obviously change as is sent in the request.
        diagnosis_keywords.document(pid).update(requestData)
        data = {
            "message": "Keywords updated",
            "pid": pid,
        }
        return data

    # This will be used while generating the prescription.
    elif(request.method == 'GET'):
        data = diagnosis_keywords.document(pid).get()
        return jsonify(data.to_dict())

    else:
        return "Invalid request"


@app.route('/')
def index():
    return "Hello world"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
