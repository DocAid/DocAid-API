from flask import Flask, redirect, url_for, request, jsonify
import pickle
import socket
import json
import numpy as np
from collections import OrderedDict
import sklearn
import random
app = Flask(__name__)


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
        diseases = ['Allergy','Cold','Dengue','Fungal_infection','Malaria','Migrane','Pneumonia','Typhoid','Urinary_tract_infection','Tuberculosis']
        symptoms = []
        for i in range(0,10):
            if data[i] == 1:
                symptoms.append(s[i])
        model = pickle.load(open('medpredMLP.pickle', 'rb'))
        # dummydata = model.predict([data])
        # d = str(dummydata[0])
        # print(type(d), d)
        with open('Medicine.json') as json_file:
            jdata = json.load(json_file)
            # print(jdata)
        #     data = jdata[d]
        # data = jsonify(dummydata)
        
        class_probs = np.array(model.predict_proba([data]))
        i,max1 = np.argsort(np.max(class_probs,axis=0))[-1],class_probs[0][i]
        j,max2 = np.argsort(np.max(class_probs,axis=0))[-2],class_probs[0][i]
        
        # print(ddata)
        dis1 = jdata[diseases[i]][1]
        prid1 = []
        for u in dis1:
            med = dis1[u]
            priority = (med[0]-3*med[1]-7*med[2])*max1
            prid1.append(priority)
            dis1[u][-1]=priority

        print(dis1)
        np.array(prid1)
        k = np.argsort(prid1)[::-1]        
        print(k)
        # for key,values in dis1.items():
        klist = [x for x in dis1]
        # print(klist)
        flist = []
        for o in k:
            flist.append(klist[o])
        # print(flist)
        # np.sort(prid1)
        ndata = OrderedDict()
        for t in flist:
            ndata[t]=dis1[t]
            # ndata = ndata.append({t:dis1[t]})
        print(ndata)
        dis2 = jdata[diseases[j]][1]
        # print(dis2)
        prid2 = []
        for u in dis2:
            med = dis2[u]
            priority = (med[0]-3*med[1]-2*med[2])*max2
            prid2.append(priority)
            dis2[u][-1]=priority

        l = np.argsort(prid2)[::-1]
        llist = [x for x in dis2]
        # print(llist)
        fllist = []
        for o in l:
            fllist.append(llist[o])
        # print(fllist)
        # print(dis2)
        for t in fllist:
            ndata[t]=dis2[t]
        print(ndata)
        
        # ndata = {d: data}
        # list1 = []
        # list2 = []
        # list1.append(ndata)
        # list1.append(symptoms)
        np.random.seed(0)
        return json.dumps([ndata,symptoms])

if __name__ == '__main__':
    app.run(host='localhost',port=5000, debug=True)
