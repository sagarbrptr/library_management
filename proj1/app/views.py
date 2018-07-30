# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from datetime import datetime,timedelta
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO

import models
def pdf_generator(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world. ");

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


# Create your views here.
@csrf_exempt
def register(request):
    print "IN REGISTER"
    if(request.method=="GET"):
        return render(request,"register.html",{})
    #POST request
    context={}
    context['name']=request.POST['name']
    context['password']=request.POST['password']
    context['username']=request.POST['username']
    context['contact']=request.POST['contact']
    context['user_type']=request.POST['user_type']
    if(models.User.objects.filter(username=context['username']).exists()):
        context['message']="ALREADY EXIST"
        return render(request,"register.html",context)
    else:
        context["message"]="User Created"
        obj=models.User(name=context['name'],password=context['password'],username=context['username'],contact=context['contact'],user_type=context['user_type'])
        obj.save()
        return render(request,"login.html",context)

@csrf_exempt
def home(request):
    if 'username' in request.session:
        if request.session['user_type']=='librarian':
            return redirect('/librarian_dash')
        else:
            return redirect('/student_dash')
    else:
        return redirect('/login')

@csrf_exempt
def login(request):
    print "IN login"

    if 'username' in request.session:
        if request.session['user_type']=='librarian':
            return redirect('/librarian_dash')
        else:
            return redirect('/student_dash')

    else:
        if request.method == "POST":
			Username = request.POST['username']
			Password = request.POST['password']
			context = {}
			if models.User.objects.filter(username = Username,password = Password):
				obj_user = models.User.objects.get(username = Username,password = Password)
				request.session['username'] = Username
				request.session['user_type'] = obj_user.user_type
				if obj_user.user_type == "librarian":
					return redirect('/librarian_dash')
				else:
					return redirect('/student_dash')
			else:
				context['message'] = "Invalid Credentials"
				response = render(request,"login.html",context)
        else:
            response = render(request,'login.html',{})
            return response


@csrf_exempt
def librarian_dash(request):
    if('user_type' in request.session):
        if(request.session['user_type']=='librarian'):
            context={}
            obj_user=models.User.objects.get(username=request.session['username'])
            context['username']=obj_user.username
            context['name']=obj_user.name
            context['contact']=obj_user.contact
            context['user_type']=obj_user.user_type
            context['books'] = list(models.books.objects.all())
            context['bookings_list'] =[]

            date_today=datetime.today().date()

            for i in models.bookings.objects.all():
                templist={}
                templist['booking']=i
                tempdate=i.issue_date+timedelta(days=7)
                templist['fine']=str(0)
                if (date_today-tempdate).days > 0 :
                    templist['fine']=str((date_today-tempdate).days*50)

                templist['return_date']=str(tempdate)
                context['bookings_list'].append(templist)


            #sort

            def ret_date(tempobj):
                return tempobj['return_date']

            context['bookings_list'].sort(key=ret_date)
            context['returns_list']=[]

            for i in context['bookings_list']:
                if(str(i['return_date'])==str(date_today)):
                    context['returns_list'].append(i)

            context['message1']="Librarian"
            response=render(request,"librarian_dash.html",context)

            return response
    else:
        context['message']="Invalid credentials"
        return redirect("/login",context)

@csrf_exempt
def student_dash(request):
    print("in stu dash")
    context={}

    if('user_type' in request.session):
        if(request.session['user_type']=='student'):
            obj_user=models.User.objects.get(username=request.session['username'])
            context['username']=obj_user.username
            print context['username']
            context['name']=obj_user.name
            context['contact']=obj_user.contact
            context['user_type']=obj_user.user_type
            context['message1']="student"
            context['books'] = models.books.objects.all()
            context['bookings'] = models.bookings.objects.filter(username=request.session['username'])
            response=render(request,"mes.html",context)

            return response
        else:
            return render(request,"mes.html",{})
    else:
        context['message']="Invalid credentials"
        return redirect("/login",context)

@csrf_exempt
def profile(request):
    usname=request.GET['username']
    context={}
    obj_user=models.User.objects.get(username=usname)
    context['username']=obj_user.username
    context['name']=obj_user.name
    context['contact']=obj_user.contact
    context['user_type']=obj_user.user_type
    response=render(request,'profile.html',context)
    return response

@csrf_exempt
def book_details(request):

	obj_user = models.books.objects.get(id=request.GET['book_id'])
	context = {}
	context['summary'] = obj_user.summary
	context['name'] = obj_user.name
	context['author'] = obj_user.author
	context['no_of_copies'] = obj_user.no_of_copies
	context['subject'] = obj_user.subject
	context['rating'] = obj_user.star_rating
	response = render(request,'summary.html',context)
	return response

@csrf_exempt
def add_books(request):

    if (('user_type' in request.session) and (request.session['user_type']=='student')):
        return redirect('/login')
    if request.method=='POST':

		if request.POST['Name']!="":
			Name = request.POST['Name']
			Author = request.POST['Author']
			no_of_copies = request.POST['no_of_copies']
			subject = request.POST['subject']
			summary = request.POST['summary']
			context = {}
			if models.books.objects.filter(name=Name,author = Author,subject = subject).exists():
				obj_user = models.books.objects.get(name = Name,author = Author,subject = subject)
				tot_book = int(obj_user.no_of_copies)
				tot_book = tot_book + int(no_of_copies)
				models.books.objects.get(name = Name,author = Author,subject = subject).delete()
				obj_user.no_of_copies = str(tot_book)
				obj = models.books(
				name = obj_user.name,
				author = obj_user.author,
				no_of_copies = obj_user.no_of_copies,
				subject = obj_user.subject,
				summary = obj_user.summary,
				)
				obj.save()
			else:
				obj = models.books(
				name = Name,
				author = Author,
				no_of_copies = no_of_copies,
				subject = subject,
				summary = summary,
				)
				obj.save()
			response = redirect('/librarian_dash')
		else:
			context = {}
			context['message'] = "Invalid entry"
    		response = render(request,"add_books.html",context)
    else:
        response = render(request,'add_books.html',{})

    return response


@csrf_exempt
def logout(request):
	if 'username' in request.session:
		del request.session['username']
		del request.session['user_type']
	return redirect('/login')

@csrf_exempt
def issue(request):
    return render(request,'issue.html',{})

@csrf_exempt
def book_a_book(request):
    #context['no_issued_books']=request.POST['no_issued_books']
    context={}
    context['username']=request.GET['username']
    context['book_id']=request.GET['book_id']
    obj_user_student=models.User.objects.get(username=context['username'])

    bookings_till_now = models.bookings.objects.filter(username=context['username']) & (models.bookings.objects.filter(status ='Pick up')|models.bookings.objects.filter(status ='To be Returned'))

    print("book id" + context['book_id'])
    print(bookings_till_now)


    for i in bookings_till_now:
        if(str(i.book_id)==str(context['book_id'])):
            context['flag']='Unsuccessful \n Cant Issue Same book more than 1 time'
            return render(request,"booking_summary.html",context)

    if(len(bookings_till_now)>1):
        context['flag']='Unsuccessful \n Cant Issue more than 2 books'
        return render(request,"booking_summary.html",context)

    obj_user = models.books.objects.get(id=context['book_id'])
    tot_book = int(obj_user.no_of_copies)

    if(tot_book>0):
        tot_book=tot_book-1

        obj_user.no_of_copies = str(tot_book)
        obj_user.save(update_fields=['no_of_copies'])

        obj2 = models.bookings(
        book_name=obj_user.name,
        username=str(context['username']),
        book_id=str(context['book_id']),
        name=obj_user_student.name,
        )
        obj2.save()

        context['flag']='Successful'
    else:
        context['flag']='Unsuccessful \nInsufficient books'

    return render(request,"booking_summary.html",context)

def approve(request):
    obj=models.bookings.objects.get(id=request.GET['booking_id'])
    if(obj.status=='Pick up'):
        obj.status='To be Returned'

    elif(obj.status=='To be Returned'):
        obj.status='Returned'

        book_obj=models.books.objects.get(id=request.GET['book_id'])
        book_obj.no_of_copies=str(int(book_obj.no_of_copies)+1)
        book_obj.save(update_fields=['no_of_copies'])

    obj.save(update_fields=['status'])
    context={}
    context['fine']=request.GET['fine']


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world. ");

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    #Added Comment 
    #return render(request,'/pdf_generator',context)
    return redirect("/librarian_dash")
