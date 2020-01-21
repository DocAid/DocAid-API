from flask import Flask, redirect, url_for, request, jsonify, render_template
from firebase_admin import credentials, firestore, initialize_app
import pickle
import requests
from collections import OrderedDict
import socket
import json
import numpy as np
import pyrebase
import pdfkit
from skimage import io
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Arrow, Circle

from config import socketIp, serverAddr

app = Flask(__name__)
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()

config = {
  "apiKey": "AIzaSyAmAnf-0bRmvGjRkJJgpZkDiZ3nRIFlBhw",
  "authDomain": "docaid-api.firebaseapp.com",
  "databaseURL": "https://docaid-api.firebaseio.com",
  "projectId": "docaid-api",
  "storageBucket": "docaid-api.appspot.com",
  "messagingSenderId": "918014081942",
  "appId": "1:918014081942:web:827def8f7c8615204d7bb7"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

patient_details = db.collection('patient_details')
medicines_diagonized = db.collection('medicines_diagonized')
diagnosis_keywords = db.collection('diagnosis_keywords')
reports = db.collection('reportsUrl')
charts1 = db.collection('charts1')
charts2 = db.collection('charts2')


# API SUMMARY

# API1: patient_details_api [POST and GET]
# API2: diagonized_medicines_api [POST GET and PUT]
# API3: diagnosis_keywords_api [POST GET and PUT]


@app.route('/rg', methods=['POST'])
def gen_pdf():
    if request.method == 'POST':
        data = request.json
        age = data['age']
        pid = data['pid']
        dosages = data['dosages']
        # bmi = data['bmi']
        img1 = 'https://firebasestorage.googleapis.com/v0/b/docaid-api.appspot.com/o/img1.jpg?alt=media&' \
               'token=63ba5fe0-d6a7-42e9-8644-129c85725845'
        img2 = 'https://firebasestorage.googleapis.com/v0/b/docaid-api.appspot.com/o/img2.png?alt=media&' \
               'token=18f4aa32-badf-4104-9e85-693dd8a96561'
        x = render_template('r.html', pid=pid, age=age,
                            # bmi=bmi,
                            dosages=dosages, img1=img1, img2=img2)
        print(type(x))
        print(x)
        pdfkit.from_string(x, 'report1.pdf')
        report = str(pid)
        storage.child('reportsPdf/{}'.format(report)).put('report1.pdf')
        pdf_url = storage.child('reportsPdf/{}'.format(report)).get_url(None)
        data = {
            'pdf_url': pdf_url
        }
        res = reports.document(pid).set(data)
        return pdf_url


@app.route('/charts1', methods=['POST'])
def chart1():
    r = request.json
    pid = r['pid']
    print(pid)
    res = requests.get( serverAddr + '/keywords', json={'pid': pid})
    data = res.json()
    total_positive_symps = []
    i = 0
    a = 0
    for da in data:
        temp = data[da]
        for key in temp.keys():
            temp1 = temp[key]
            temp2 = temp1['symptoms']
            for k in temp2.keys():
                print(type(temp2[k]))
                if temp2[k]:
                    a += 1
            break
        i += 1
        if i % 2 == 0:
            i = 0
            total_positive_symps.append(a)
    for i in range(1, len(total_positive_symps)):
        total_positive_symps[i] = total_positive_symps[i] - total_positive_symps[i - 1]
    date_str = ['1-3', '4-6', '7-9', '10-12', '13-15', '16-18', '19-21', '22-24']
    print(total_positive_symps)
    print(date_str)

    plt.plot(date_str, total_positive_symps,
             label="No of symptoms recognized per 3 days", marker="*", color='green', linestyle='dashed', linewidth=3,
             markerfacecolor='blue', markersize=12)

    # setting x and y axis range
    plt.ylim(1, 32)
    plt.xlim(1, 8)
    # naming the x axis
    plt.xlabel('Date intervals')
    # naming the y axis
    plt.ylabel('Number of positive symptoms')
    plt.legend()
    # giving a title to my graph
    plt.title('Positive predicted symptoms acc to date')
    plt.savefig('plot1.png')
    report = str(pid)
    storage.child('charts1/{}'.format(report)).put('plot1.png')
    chart_url = storage.child('charts1/{}'.format(report)).get_url(None)
    data = {
        'chart_url': chart_url
    }
    # res = charts1.document(pid).set(data)
    return data


@app.route('/charts2', methods=['POST'])
def charts2():
    r = request.json
    pid = r['pid']
    res = requests.get(
        serverAddr + '/diagonized_medicines', json={'pid': 'POC008'})
    data = res.json()
    doxyl = 0
    vist = 0
    xyzal = 0
    other = 0
    levoce = 0
    for d in data:
        x = data[d]['medicines']
        for i in x:
            if i['name'] == 'doxylamine':
                doxyl += i['dosage']
            elif i['name'] == 'vistaril':
                vist += i['dosage']
            elif i['name'] == 'Xyzal':
                xyzal += i['dosage']
            elif i['name'] == 'levocetirizili':
                levoce += i['dosage']
            else:
                other += i['dosage']

    x = [doxyl, vist, xyzal, levoce, other]
    y = ["doxylamine", "vistaril", 'Xyzal', 'levocetirizili', 'other']

    colors = ['r', 'y', 'g', 'b', 'm']

    # plotting the pie chart
    plt.pie(x, labels=y, colors=colors,
            startangle=90, shadow=True, explode=(0.1, 0.1, 0.1, 0.1, 0),
            radius=1.2, autopct='%1.1f%%', pctdistance=1.1, labeldistance=1.3),
    handles = []
    for i, l in enumerate(y):
        handles.append(matplotlib.patches.Patch(color=colors[0], label=l))

    plt.legend(handles, y, bbox_to_anchor=(0.9, 1.025), loc="upper left")
    plt.title('Doasges or tablets taken for each medicine in a week\n\n')
    plt.savefig('plot2.png')
    report = str(pid)
    storage.child('charts2/{}'.format(report)).put('plot2.png')
    chart_url = storage.child('charts2/{}'.format(report)).get_url(None)
    data = {
        'chart_url': chart_url
    }
    # temp = pid + "pie"
    # res = charts1.document(temp).set(data)
    return data


@app.route('/charts3', methods=['POST'])
def charts3():
    r = request.json
    pid = r['pid']
    print(pid)
    res = requests.get(
        serverAddr + '/patient_details', json={'pid': pid})
    data = res.json()
    print(data)
    weight = data['weight']
    height = data['height']
    maze = io.imread(
        'https://www.chartsgraphsdiagrams.com/HealthCharts/images/bmi-status-metric.png')
    cx = int(weight)  # Kg
    cy = int(height)  # cm

    patches = [Circle((cy, cx), radius=25, color='green')]
    fig, ax = plt.subplots(1)
    plt.axis('off')
    ax.imshow(maze)
    for p in patches:
        ax.add_patch(p)
    plt.title('BMI on the BMI Graph, Marker represents the BMI location.')
    plt.savefig('ans.png')
    report = str(pid)
    storage.child('charts3/{}'.format(report)).put('ans.png')
    chart_url = storage.child('charts3/{}'.format(report)).get_url(None)
    data = {
        'chart_url': chart_url
    }
    # temp = pid + "bmi"
    # res = charts1.document(temp).set(data)
    return data


@app.route('/sendReportToDB', methods=['POST'])
def get_report():
    request_data = request.json
    pid = request_data['pid']
    data = reports.document(pid).get()
    return jsonify(data.to_dict())


@app.route('/prediction', methods=['POST'])
def prediction():
    # global i
    request_data = request.json
    print(request_data)
    data = request_data['val']
    patient = request_data['patient']
    if request.method == 'POST':
        s = ['skin_rash', 'continuous_sneezing', 'acidity', 'fatigue', 'nausea', 'loss_of_appetite',
             'chest_pain', 'fast_heart_rate', 'bladder_discomfort', 'muscle_pain', 'prognosis']
        diseases = ['Allergy', 'Cold', 'Dengue', 'Fungal infection', 'Malaria',
                    'Migraine', 'Pneumonia', 'Typhoid', 'Urinary tract infection', 'Tuberculosis']
        symptoms = []
        alcohol = patient['alc']
        pregnancy = patient['preg']
        for i in range(0, 10):
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
            data = data[1]
            print("Before JSON: ", data)
            result = [data, symptoms]
            print(result)
            return pickle.dumps(result)

        # class_probs = np.array(model.predict_proba([data]))
        # i, max1 = np.argsort(np.max(class_probs, axis=0)
        #                      )[-1], class_probs[0][i]
        # j, max2 = np.argsort(np.max(class_probs, axis=0)
        #                      )[-2], class_probs[0][i]
        #
        # # print(ddata)
        # dis1 = jdata[diseases[i]][1]
        # prid1 = []
        # for u in dis1:
        #     med = dis1[u]
        #     priority = (med[0] - 3 * alcohol - 7 * pregnancy) * max1
        #     prid1.append(priority)
        #     dis1[u][-1] = priority
        #
        # print(dis1)
        # np.array(prid1)
        # k = np.argsort(prid1)[::-1]
        # print(k)
        # # for key,values in dis1.items():
        # klist = [x for x in dis1]
        # # print(klist)
        # flist = []
        # for o in k:
        #     flist.append(klist[o])
        # # print(flist)
        # # np.sort(prid1)
        # ndata = OrderedDict()
        # for t in flist:
        #     ndata[t] = dis1[t]
        #     # ndata = ndata.append({t:dis1[t]})
        # print(ndata)
        # dis2 = jdata[diseases[j]][1]
        # # print(dis2)
        # prid2 = []
        # for u in dis2:
        #     med = dis2[u]
        #     priority = (med[0] - 3 * alcohol - 2 * pregnancy) * max2
        #     prid2.append(priority)
        #     dis2[u][-1] = priority
        #
        # l = np.argsort(prid2)[::-1]
        # llist = [x for x in dis2]
        # # print(llist)
        # fllist = []
        # for o in l:
        #     fllist.append(llist[o])
        # # print(fllist)
        # # print(dis2)
        # for t in fllist:
        #     ndata[t] = dis2[t]
        # print(ndata)
        #
        # # ndata = {d: data}
        # # list1 = []
        # # list2 = []
        # # list1.append(ndata)
        # # list1.append(symptoms)
        # np.random.seed(0)



@app.route('/patient_details', methods=['POST', 'GET'])
def patient_details_api():

    request_data = request.json
    pid = request_data['pid']

    if request.method == 'POST':
        # res = patient_details.document(pid).set(request.json)
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


@app.route('/diagonized_medicines_1', methods=['POST'])
def diagonalized_medicines_1():
    request_data = request.json
    pid = request_data['pid']

    if request.method == 'POST':
        data = medicines_diagonized.document(pid).get()
        d = data.to_dict()
        l = []
        for key in d:
            l.append(d[key])
        return jsonify(data.to_dict())
    else:
        return "Invalid request"


@app.route('/diagonized_medicines', methods=['POST', 'GET', 'PUT'])
def diagonalized_medicines():
    request_data = request.json
    pid = request_data['pid']
    if request.method == 'POST':

        timestamp = request_data['timestamp']
        send_data = {timestamp: request_data}
        medicines_diagonized.document(pid).set(send_data)
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

            #Thats just json, manipulation, in the api, we will just update the value, whenever a put request is 
            received.
        '''
        # The request_data will obviously change as is sent in the request.

        timestamp = request_data['timestamp']
        data = medicines_diagonized.document(pid).get()
        data = data.to_dict()
        json_data = {}
        for key in data.keys():
            json_data[key] = data[key]
        json_data[timestamp] = request_data
        print(json_data)
        medicines_diagonized.document(pid).update(json_data)
        data = {
            "message": "Medicines updated",
            "pid": pid,
        }
        return data

    # This will be used while generating the prescription.
    elif request.method == 'GET':
        data = medicines_diagonized.document(pid).get()
        return jsonify(data.to_dict())

    else:
        return "Invalid request"


@app.route('/keywords', methods=['GET', 'PUT', 'POST'])
def keywords():
    request_data = request.json
    pid = request_data['pid']

    if request.method == 'POST':
        timestamp = request_data['timestamp']
        send_data = {timestamp: request_data}
        diagnosis_keywords.document(pid).set(send_data)
        data = {
            "message": "Keywords stored!!!",
            "pid": pid,
            "timestamp": timestamp
        }
        return data

    elif request.method == 'PUT':
        '''
            This is exactly same as the previous API.

            Now this is interesting, please note carefully. 
            When the doctor is gonna update it when the user visits second time, 
            Here, the previous json object will be called using get and then the current one will be appended,
            so that it becomes an array of objects according to timestamp. 

            That's just json, manipulation, in the api, we will just update the value, whenever a put request is 
            received.
        '''
        # The requestData will obviously change as is sent in the request.

        timestamp = request_data['timestamp']
        data = diagnosis_keywords.document(pid).get()
        print(data)
        data = data.to_dict()
        json_data = {}
        print(data)
        for key in data.keys():
            json_data[key] = data[key]
        print(json_data)
        json_data[timestamp] = request_data
        diagnosis_keywords.document(pid).update(json_data)
        data = {
            "message": "Keywords updated",
            "pid": pid,
        }
        return data

    # This will be used while generating the prescription.
    elif request.method == 'GET':
        data = diagnosis_keywords.document(pid).get()
        return jsonify(data.to_dict())

    else:
        return "Invalid request"


@app.route('/', methods=['GET'])
def index():
    return "Welcome to DocAid-API"


@app.route('/socket_conn', methods=['POST'])
def socket_server():
    # Work for raghav: pull user data from firebase and put it in data
    # if data not in firebase, return unsuccessful

    data = request.json
    pid = data['pid']
    client.send(pickle.dumps(pid))
    return "Hello World"


if __name__ == '__main__':
    host = socketIp
    port = 5500

    client = socket.socket()
    client.connect((host, port))
    app.run(host='0.0.0.0', debug=True)
