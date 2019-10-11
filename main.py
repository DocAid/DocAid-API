
from flask import Flask, redirect, url_for, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import pickle
import socket
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
        s = ['skin_rash','continuous_sneezing','acidity','fatigue','nausea','loss_of_appetite','chest_pain','fast_heart_rate','bladder_discomfort','muscle_pain','prognosis']
        symptoms = []
        for i in range(0,10):
            if data[i] == 1:
                symptoms.append(s[i])
        model = pickle.load(open('medpredMLP.pickle', 'rb'))
        dummydata = model.predict([data])
        d = str(dummydata[0])
        print(type(d), d)
        with open('Medicine.json') as json_file:
            jdata = json.load(json_file)
            # print(jdata)
            data = jdata[d]
        # data = jsonify(dummydata)
        print(type(data))
        ndata = {d: data}
        print(type(ndata))
        list1 = []
        list1.append(ndata)
        list1.append(symptoms)
        jsondata = jsonify(list1)
        return jsondata


@app.route('/patient_details', methods=['POST', 'GET'])
def patient_details_api():

    requestData = request.json
    pid = requestData['pid']

    if request.method == 'POST':
        res = patient_details.document(pid).set(request.json)
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



@app.route('/diagonized_medicines_1',methods=['POST'])
def diagonized_medicines_1():
    requestData = request.json
    pid = requestData['pid']

    if(request.method == 'POST'):
        data = medicines_diagonized.document(pid).get()
        d = data.to_dict()
        l = []
        for key in d:
            l.append(d[key])
        return jsonify(data.to_dict())
    else:
        return "Invalid request"

@app.route('/diagonized_medicines', methods=['POST', 'GET', 'PUT'])
def diagonized_medicines():
    requestData = request.json
    pid = requestData['pid']
    if(request.method == 'POST'):

        timestamp = requestData['timestamp']
        sendData = {}
        sendData[timestamp] = requestData
        medicines_diagonized.document(pid).set(sendData)
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

        timestamp = requestData['timestamp']
        data = medicines_diagonized.document(pid).get()
        data = data.to_dict()
        json_data = {}
        for key in data.keys():
            json_data[key] = data[key]
        json_data[timestamp] = requestData
        print(json_data)
        medicines_diagonized.document(pid).update(json_data)
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


@app.route('/keywords', methods=['GET', 'PUT', 'POST'])
def keywords():

    requestData = request.json
    pid = requestData['pid']

    if(request.method == 'POST'):
        timestamp = requestData['timestamp']
        sendData = {}
        sendData[timestamp] = requestData
        diagnosis_keywords.document(pid).set(sendData)
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

        timestamp = requestData['timestamp']
        data = diagnosis_keywords.document(pid).get()
        print(data)
        data = data.to_dict()
        json_data = {}
        print(data)
        for key in data.keys():
            json_data[key] = data[key]
        print(json_data)
        json_data[timestamp] = requestData
        diagnosis_keywords.document(pid).update(json_data)
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
    return "Welcome to DocAid-API"


@app.route('/socket_conn', methods=['GET'])
def socket_server():

    # Work for raghav: pull user data from firebase and put it in data
    # if data not in firebase, return unsuccessful

    data = request.json
    pid = data['pid']
    data = patient_details.document(pid).get()
    data = jsonify(data.to_dict())
    client.send(data.encode())
    return "Hello World"


if __name__ == '__main__':
    app.run(debug=True)
#     host = "34.93.126.224"
#     port = 5500

#     client = socket.socket()
#     client.connect((host, port))
#     app.run(host='0.0.0.0', port=5000, debug=True)
