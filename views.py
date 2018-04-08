# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.shortcuts import render
from django.http import HttpResponse
from django.core import validators


from rest_framework import viewsets

import ctypes
import json
import datetime as dt
from . import handy, models
#from handy import *
from models import *
from handy import *

# Create your views here.
# to be garnished with validators

class TheView (viewsets.ViewSet):

    def view(self,request,*args,**kwargs):

        

        self.message = json.loads(request.POST['message'])

        if not self.message:
            return HttpResponse('message missing')

        self.patientId = self.message['patientId']
        self.patientName= self.message['patientName']
        self.mrn = self.message['mrn']
        self.dob = self.message['dob']
        self.targetUser = self.message['targetUser']
        self.alertCode = self.message['alertCode']
        self.text = self.message['text']
        self.timeStamp = self.message['timeStamp']
        self.module = self.message['module']
        self.encounter = self.message['encounter']
        self.encounterAlias = self.message['encounterAlias']
        self.encounerDisplay = self.message['encounerDisplay']

        if args:
            self.text = args[0]['myText']
            
        
        self.patientObj = Patient.objects.get_or_create(

        patient_foreignId =  float(self.patientId)  ,
        patient_name = self.patientName ,
        patient_alias = self.mrn ,
        patient_dob = dt.datetime.strptime(self.dob,"%Y%m%d")

        )[0]
        self.patientObj.save()

        self.alertObj = Alert_Definition.objects.get(

        alert_code = int(self.alertCode) 

        )

        self.userObj = User.objects.get_or_create(

        user_foreignId = float(self.targetUser)
        )[0]

        self.userObj.save()

        self.encounterObj = Encounter.objects.get_or_create(

        encounter_foreignId = float(self.encounter),
        encounter_alias = self.encounterAlias,
        encounter_type = self.encounerDisplay,
        patient_identifier= self.patientObj

        )[0]

        self.rawIssueObj = Raw_Issue.objects.create(

        patient_identifier = self.patientObj,
        date = dt.datetime.strptime(self.timeStamp,"%Y%m%d%H%M%S"),
        module = self.module,
        alert_code = self.alertObj,
        text = self.text,
        user_identifier = self.userObj,
        encounter_identifier = self.encounterObj
        
        )
        #self.rawIssueObj.save()

        

        return HttpResponse('success')


    def browse(self,request):

        contexter = {'alerts':DetectedIssue.objects.all()}

        return render(request, 'docView.html', contexter)


class MASCC(viewsets.ViewSet):

    def MASCCView(self, request):

        self.message = json.loads(request.POST['message'])

        if not self.message:
            return HttpResponse('message missing')

        self.patientId = self.message['patientId']
        self.patientName= self.message['patientName']
        self.mrn = self.message['mrn']
        self.dob = self.message['dob']
        self.targetUser = self.message['targetUser']
        self.alertCode = self.message['alertCode']
        #self.text = self.message['text']
        self.timeStamp = self.message['timeStamp']
        self.module = self.message['module']
        self.encounter = self.message['encounter']
        self.encounterAlias = self.message['encounterAlias']
        self.encounerDisplay = self.message['encounerDisplay']
        self.anc = self.message['neutrophilsCount']
        self.temp = self.message['temperature']
        self.sbp = self.message['sbp']
        self.problemList = self.message['problemList']

        self.score= 0

        if self.anc and self.temp:
            if self.anc <= 0.5 and self.temp > 37: self.score += 5
            elif self.anc <= 0.5 and self.temp > 39: self.score += 3
        
        if self.sbp:
            if self.sbp > 90: self.score += 5
        
        self.ageYrs =  (dt.datetime.today()).year - (dt.datetime.strptime(self.dob,"%Y%m%d")).year

        if self.ageYrs:
            if self.ageYrs < 60: self.score +=2

        if self.encounerDisplay:
            if self.encounerDisplay == 'O': self.score +=3
        
        '''deydration requiring parenteral intervention assuming it is documented on those codes'''
        self.dehydrationInd = dict(set((self.problemList).items()).intersection(set(dehydrationCodes.items())))
        if not self.dehydrationInd:
            self.score +=3

        '''chronic obstructive pulmonary disorder assuming it is documented using those codes'''
        self.pulmonaryInd = dict(set((self.problemList).items()).intersection(set(chronicObstructivePulmonaryCodes.items())))
        if not self.pulmonaryInd:
            self.score +=4

        '''solid tumor assuming it is documented using those codes'''
        self.solidTumorInd = dict(set((self.problemList).items()).intersection(set(solidTumorCodes.items())))

        '''hematology disease assuming it is documented using those codes'''
        self.hematologyInd = dict(set((self.problemList).items()).intersection(set(hematologyCodes.items())))

        '''past fungal infection assuming it is documented using those codes'''
        self.fungalInfectionInd = dict(set((self.problemList).items()).intersection(set(fungalInfectionCodes.items())))

        if self.solidTumorInd or self.hematologyInd:
            if not self.fungalInfectionInd:
                self.score += 4
        
        

        myText= 'MASCC Score is {}'.format(self.score)
        
        instancer = TheView()
        instancer.view(request,{'myText':myText})


        return HttpResponse('Score is {}'.format(self.score))

        


        



        

        
