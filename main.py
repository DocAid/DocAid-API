
from flask import Flask, redirect, url_for, request, jsonify, render_template
from firebase_admin import credentials, firestore, initialize_app

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


@app.route('/patient_details_api', methods=['POST', 'GET'])
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


@app.route('/diagonized_medicines_api', methods=['POST', 'GET', 'PUT'])
def diagonized_medicines_api():
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


@app.route('/', methods=["GET"])
def index():
    return "HEllo world"


@app.route('/diagnosis_keywords_api', methods=['GET', 'PUT', 'POST'])
def diagnosis_keywords_api():

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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
