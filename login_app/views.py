from django.shortcuts import render, redirect
from django.contrib import messages
from book_app.models import *
import bcrypt
import book_app.urls
# Create your views here.

def index(request):

	return render(request, 'index.html')


def addition(request):
	errors = User.objects.basic_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/")

	if not User.objects.filter(first_name = request.POST['first_name'], last_name = request.POST['last_name'],
		email = request.POST['email']).exists():
		password = request.POST['password']
		pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
		User.objects.create(first_name =request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password =pw_hash )

	return redirect('/')

def check(request):

	errors = User.objects.login_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/")

	user = User.objects.filter(email = request.POST['email'])

	if user:
		logged_user = user[0]
		if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
			request.session['userid'] = logged_user.id

			return redirect('/books')
	return redirect('/')






