# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime,timedelta

# Create your models here.
user_choices=[
    ('librarian','librarian'),
    ('student','student'),
]

class User(models.Model):
    name=models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    contact=models.CharField(max_length=50)
    user_type=models.CharField(max_length=50,choices=user_choices,default='librarian')

    def __str__(self):
        return self.name

class books(models.Model):
    name=models.CharField(max_length=50)
    author=models.CharField(max_length=50)
    no_of_copies=models.IntegerField()
    summary=models.CharField(max_length=300,default='default')
    star_rating=models.IntegerField(default=1)
    subject=models.CharField(max_length=300,default='subject')

    def __str__(self):
        return self.name + " " + self.author + " " + str(self.no_of_copies)

class bookings(models.Model):
    book_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    book_id=models.IntegerField()
    name=models.CharField(max_length=50)
    status=models.CharField(max_length=50,default='Pick up')
    issue_date=models.DateField(default=datetime.today())

    def __str__(self):
        return str(self.book_name) + " " + str(self.book_id) + " " + str(self.username)
