from flask import Flask, redirect, url_for,request,jsonify
from firebase_admin import credentials, firestore, initialize_app
app = Flask(__name__)



cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()

patient_details = db.collection('patient_details')
medicines_diagonized = db.collection('medicines_diagonized')



'''
    API 1:
        - This has two types,
            1. POST Request.
                The params are sent and stored in the firebase.
            2. GET Request.
        
        #Please note that in both of them the mandatory parameter is the patient id, that can be easily and randomly generated for a particular user
        #This will basically function as the primary key in all the collections.
'''

@app.route('/patient_details',methods=['POST','GET'])
def patient_details():

    requestData = request.json
    pid = requestData['pid']

    if request.method == 'POST':
        res = patient_details.document(pid).set(request.json)
        data = {
            "message":"patient_added",
            "pid": pid 
        }
        return data
    elif request.method == 'GET':
        data = patient_details.document(pid).get()
        return jsonify(data.to_dict())
    else:
        return "Invalid request"
    

'''
    API 2:
        - This has three types,
            1. POST Request.
                The params are sent and stored in the firebase, medicines and all.
                Here timestamp and pid are the compulsory params.
            2. GET Request.
                Just give the pid and get all the medicines prescribed.
            3. PUT request
                Here, we have o provide the pid with the !!UPDATED JSON!!
                #Please read the documentation below for the updated json task.

        #Please note that in both of them the mandatory parameter is the patient id, that can be easily and randomly generated for a particular user
        #This will basically function as the primary key in all the collections.
'''



@app.route('/diagonized_medicines',methods=['POST','GET','PUT'])
def diagonized_medicines():
    requestData = request.json
    pid = requestData['pid']

    if(request.method == 'POST'):
        timestamp = requestData['timestamp']
        medicines_diagonized.document(pid).set(request.json)
        data = {
                "message":"Medicines stored for first time",
                "pid": pid,
                "timestamp":timestamp
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
        #The requestData will obviously change as is sent in the request.
        medicines_diagonized.document(pid).update(requestData)
        data = {
            "message":"Medicines updated",
            "pid":pid,
        }
        return data

    elif(request.method == 'GET'):
        data = medicines_diagonized.document(pid).get()
        return jsonify(data.to_dict())

    else:
        return "Invalid request"


if __name__ == '__main__':
   app.run(debug = True)
