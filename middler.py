import hl7
import requests as re
import json
import datetime as dt
import hl7apy.parser as hl

'''NDS Message'''

message = 'MSH|^~\&|CERNER|57357|MIDDLEWARE|MIDDLER|201803262000||NDS|CNTRL-0001|P|2.4\r'
message+= 'PID|1|103457|103456||Stanley^Tim^^||20010429|M|2||19 Ray St^^Alba^^532^UK|||||M|CHR||46264212||||London|Y||\r'
message+= 'PV1|1|I|CARE POINT^5^1^Instate^^C|R||||||||||||N|||8573245|||||||||||||||||||||||||200911011122||||||12\r'
message+= 'NDS|1|201803262000|C|2|2|patient is at Braden Q score of 9 and he is on a NSAID (diclofenac potassium)|Braden Q-NSAIDs'

#placing text as notification details field 6
#placing eks module as notification details field 7
#placing physician to be notified id as notification details field 5
#placing encounter alias as alternative visit no. field 50

pmes= hl7.parse(message)
namer = (str(pmes[1][5][0])).split('^')
name = namer[1]+' '+namer[0]

params = {
    'patientId':str(pmes[1][2][0]),
    'patientName': name,
    'mrn' : str(pmes[1][9][0]),
    'dob' : str(pmes[1][7][0]),
    'targetUser' : str(pmes[3][5][0]),
    'alertCode' : str(pmes[3][4][0]),
    'text': str(pmes[3][6][0]),
    'timeStamp': str(pmes[3][2][0]),
    'module': str(pmes[3][7][0]),
    'encounter': str(pmes[2][19][0]),
    'encounterAlias': str(pmes[2][50][0]),
    'encounerDisplay': str(pmes[2][2][0])
    

          }

params = json.dumps(params)

#reqme = re.post('http://127.0.0.1:8000/main/',data = {'message':params})

#print reqme

'''ORU Message'''
obsmessage = 'MSH|^~\&|CERNER|57357|MIDDLEWARE|MIDDLER|201803262000||ORU|CNTRL-0001|P|2.4\r'
obsmessage+= 'PID|1|1034505|1105005||Conner^Sara^^||19810430|M|2||19 Ray St^^Alba^^532^UK|||||M|CHR||46264216||||London|Y||\r'
obsmessage+= 'PV1|1|I|CARE POINT^5^1^Instate^^C|R||||||||||||N|||857333|||||||||||||||||||||||||200911011125||||||12\r'
obsmessage+= 'OBR |1 | |VS12340000 |3 ^risk of CVS Problem||||||||||||||1\r'
obsmessage+= 'OBX|1|TX|127||patient at risk of CVS SCORE is 15_ smoker, familial HTN, hyperlipidemic|||||||||20180407120000'

obs= hl7.parse(obsmessage)
obsnamer = (str(obs[1][5][0])).split('^')
obsname = obsnamer[1]+' '+obsnamer[0]

obsparams = {
    
    'patientId':str(obs[1][2][0]),
    'patientName': obsname,
    'mrn' : str(obs[1][9][0]),
    'dob' : str(obs[1][7][0]),
    'targetUser' : str(obs[3][18][0]),
    'alertCode' : str(obs[3][4][0]).split('^')[0].strip(),
    'text': str(obs[4][5][0]),
    'timeStamp': str(obs[4][14][0]),
    'module': str(obs[3][4][0]).split('^')[1],
    'encounter': str(obs[2][19][0]),
    'encounterAlias': str(obs[2][50][0]),
    'encounerDisplay': str(obs[2][2][0])
    

          }

obsparams = json.dumps(obsparams)

#reqme = re.post('http://127.0.0.1:8000/main/',data = {'message':obsparams})

#print reqme

'''MASCC message'''
masMessage = 'MSH|^~\&|HL7Soup|Instance1|HL7Soup|Instance2|20180406170000||??????|64322|P|2.5.1\r'
masMessage += 'PID|1|103456|103456||Stanley^Jim^^||19780429|M|||19 Raymond St^^Albany^^5632^UK|||||M|CHR||46264212||||London|Y\r'
masMessage += 'PV1|1|O|CARE POINT^5^1^Instate^^C|R||||||||||||N|||857333|||||||||||||||||||||||||200911011125||||||12\r'
masMessage+= 'OBR |1|||4^MASCC||||||||||||||1\r'
masMessage += 'OBX|1|NM|123||500|m3||||||||20180406170000\r'
masMessage += 'OBX|1|NM|124||39|celsius degrees||||||||20180406170000\r'
masMessage += 'OBX|1|NM|125||90|MMHG||||||||20180406170000\r'
masMessage += 'PRB|UC|20180106120000|55342001^Neoplastic disease^SNOMED CT|1|||200911021022\r'
masMessage += 'PRB|UC|20180106120000|1601000119105^Moderate dehydration^SNOMED CT|1|||200911021022'

mas = hl7.parse(masMessage)
masNamer = (str(mas[1][5][0])).split('^')
masName = masNamer[1]+' '+masNamer[0]

problemList = {}

problemList = {str(i[3]).split('^')[0]:str(i[3]).split('^')[1] for i in mas['PRB']}




masparams = {

    'patientId':str(mas[1][2][0]),
    'patientName': masName,
    'mrn' : str(mas[1][9][0]),
    'dob' : str(mas[1][7][0]),
    'targetUser' : str(mas[3][18][0]),
    'alertCode' : str(mas[3][4][0]).split('^')[0].strip(),
    'text': '',
    'timeStamp': str(mas[0][7][0]),
    'module': str(mas[3][4][0]).split('^')[1],
    'encounter': str(mas[2][19][0]),
    'encounterAlias': str(mas[2][50][0]),
    'encounerDisplay': str(mas[2][2][0]) ,
    'neutrophilsCount': str(mas[3][4][0]) ,
    'temperature':str(mas[4][4][0]) ,
    'sbp': str(mas[5][4][0]),
    'problemList':problemList


    }
masparams = json.dumps(masparams)

reqme = re.post('http://127.0.0.1:8000/mascc/',data = {'message':masparams})

print reqme
