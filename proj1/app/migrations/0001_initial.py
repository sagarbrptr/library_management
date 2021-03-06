# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-23 18:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='bookings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('book_id', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('status', models.CharField(default='Pick up', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='books',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50)),
                ('no_of_copies', models.IntegerField()),
                ('summary', models.CharField(default='default', max_length=300)),
                ('star_rating', models.IntegerField(default=1)),
                ('subject', models.CharField(default='subject', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('contact', models.CharField(max_length=50)),
                ('user_type', models.CharField(choices=[('librarian', 'librarian'), ('student', 'student')], default='librarian', max_length=50)),
                ('no_issued_books', models.IntegerField(default=0)),
            ],
        ),
    ]
