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

# Create your views here.
# to be garnished with validators

class TheView (viewsets.ViewSet):

    def view(self,request):

        

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





        

        
