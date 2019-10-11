def feature_val(string):

    s = ['skin_rash','continuous_sneezing','acidity','fatigue','nausea','loss_of_appetite','chest_pain','fast_heart_rate','bladder_discomfort','muscle_pain','prognosis']
    s = ['rash','skin','sneeze','cold','acid','acidity','fatigue','nausea','loss','appetite','chest','pain','heart_rate','bladder','discomfort','muscle','pain']
    map_dict = {
        s[0]:set(['rash','skin','rashes','redmarks','itching','irritation','skinburn']),
        s[1]:set(['sneeze','sneezing','cold','cough']),
        s[2]:set(['acid','acidity','burning','stomach ache','stomach pain','digestion']),
        s[3]:set(['fatigue','tired','tiredness','hypertension','alwayslazy','lazy','variness','lethargy','drowsiness']),
        s[4]:set(['nausea','vomiting','sickness','puking','motion sickness','morning sickness']),
        s[5]:set(['appetite loss','lazy','sick','tired']),
        s[6]:set(['chest']),
        s[7]:set(['heart rate','rate','breath']),
        s[8]:set(['urine','bladder','excretion','restless']),
        s[9]:set(['muscle','body'])
    }


    arr = string.split(" ")
    precidtion_values= [0,0,0,0,0,0,0,0,0,0]
    for element in arr:
        for i in range(0,10):
            if element in map_dict[s[i]]:
                precidtion_values[i] = 1


    return precidtion_values