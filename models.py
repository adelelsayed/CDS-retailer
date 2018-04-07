# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.core.mail import send_mail

# Create your models here.
'''yet to add methods to classes'''

class Patient (models.Model):

    patient_identifier = models.AutoField(primary_key=True)
    patient_foreignId = models.FloatField()
    patient_name = models.CharField(max_length=264)
    patient_alias = models.CharField(max_length=264)
    patient_dob = models.DateTimeField(null = True)
    active_ind = models.BooleanField(default=True)
    updt_id = models.ForeignKey('User',default=1,related_name = 'patient')
    updt_dt_tm = models.DateTimeField(auto_now=True)


class User (models.Model):

    user_identifier =  models.AutoField(primary_key=True)
    user_foreignId = models.FloatField()
    user_name = models.CharField(max_length=264)
    user_position = models.CharField(max_length=264)
    connection = models.CharField(max_length=264)
    active_ind = models.BooleanField(default=True)
    process_flag = models.BooleanField(default=False)
    updt_id = models.IntegerField(default=1)
    updt_dt_tm = models.DateTimeField(auto_now=True)

class Encounter (models.Model):

    encounter_identifier = models.AutoField(primary_key=True)
    encounter_foreignId = models.FloatField()
    encounter_alias = models.CharField(max_length=264)
    encounter_type = models.CharField(max_length=264)
    updt_id = models.ForeignKey('User',default=1, related_name = 'enc_updt_id')
    updt_dt_tm = models.DateTimeField(auto_now=True)
    patient_identifier =  models.ForeignKey('Patient',related_name='patient')


class Alert_Definition(models.Model):

    alert_code = models.AutoField(primary_key=True)
    alert_title = models.CharField(max_length=264)
    category = models.CharField(max_length=264)
    severity = models.CharField(max_length=264)
    active_ind = models.BooleanField(default=True)
    updt_id = models.ForeignKey('User',default=1, related_name='alert_def_updter')
    updt_dt_tm = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.alert_code) + ' ' + self.alert_title

class DetectedIssue (models.Model):

    identifier = models.AutoField(primary_key=True)
    reference = models.CharField(max_length=264)
    implicated = models.IntegerField(default=0)
    detail = models.CharField(max_length=264)
    encounter_identifier = models.ForeignKey('Encounter')
    status = models.CharField(max_length=264)
    category = models.CharField(max_length=264)
    severity = models.CharField(max_length=264)
    patient_identifier = models.ForeignKey('Patient')
    author =  models.ForeignKey('User',default=1)
    date =  models.DateTimeField()
    raw_issue_id = models.ForeignKey('Raw_Issue')
    active_ind = models.BooleanField(default=True)
    updt_id = models.ForeignKey('User',default=1, related_name = 'issue_updter')
    updt_dt_tm = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.identifier) + ' '+ str(self.raw_issue_id)


class Raw_Issue (models.Model):

    raw_issue_id = models.AutoField(primary_key=True)
    patient_identifier = models.ForeignKey('Patient')
    date = models.DateTimeField()
    module = models.CharField(max_length=264)
    alert_code = models.ForeignKey('Alert_Definition')
    text = models.TextField()
    user_identifier = models.ForeignKey('User',related_name ='issue_to_be_notified_prsnl')
    encounter_identifier =  models.ForeignKey('Encounter')
    active_ind = models.BooleanField(default=True)
    process_flag = models.BooleanField(default=False)
    updt_id = models.ForeignKey('User',default=1, related_name='raw_updter')
    updt_dt_tm = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.raw_issue_id)


def generator(sender, instance, *args, **kwargs):

    #alertDef =  (instance.alert_code).values()[0]

    issue = DetectedIssue.objects.create(

detail=instance.text,
encounter_identifier = instance.encounter_identifier,
status = 'final',
category = (instance.alert_code).category,
severity = (instance.alert_code).severity,
patient_identifier = instance.patient_identifier,
date = instance.date,
raw_issue_id=instance


    
    )
    
       

post_save.connect(generator,sender=Raw_Issue)


