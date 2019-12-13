from django.shortcuts import render, redirect
from django.contrib import messages
from book_app.models import *
import bcrypt
import login_app.urls

# Create your views here.

def book(request):
	if 'userid' in request.session:

		books = Book.objects.all()
		userid = request.session['userid']
		user = User.objects.get(id = userid)
		liked_lists = user.liked_books.all()
		titles = []
		for liked_list in liked_lists:
			titles.append(liked_list.title)


		context = {
		'books' : books,
		'user' : user,
		'userid' : userid,
		'titles' : titles,
		}
		return render(request, 'book.html', context)
	else:
		return redirect('/')


def add_book(request):
	user = User.objects.get(id = request.session['userid'])
	errors = Book.objects.basic_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/books")

	if not Book.objects.filter(title = request.POST['title']).exists():
		new = Book.objects.create(title =request.POST['title'], desc = request.POST['desc'],uploaded_by = user)
		new.users_who_like.add(user)

	return redirect('/books')

def book_id(request, num):
	book = Book.objects.get(id = num)
	liked_users = book.users_who_like.all()
	user = User.objects.get(id = request.session['userid'])

	context = {
	'book' : book,
	'liked_users':liked_users,
	"boolean" : User.objects.get(id = request.session['userid']) ==  book.uploaded_by,
	'user' : user,
	}

	return render(request, 'book_id.html', context)


def add_to_favorite(request, num):
	user = User.objects.get(id = request.session['userid'])
	Book.objects.get(id = num).users_who_like.add(user)

	return redirect('/books')

def delete(request,num):
	book = Book.objects.get(id = num)
	book.delete()

	return redirect("/books")

def unfavorite(request, num):
	book = Book.objects.get(id = num)
	user = User.objects.get(id = request.session['userid'])
	book.users_who_like.remove(user)
	return redirect('/books/{}'.format(num))

def edit(request, num):
	errors = Book.objects.basic_validator(request.POST)
	if len(errors)>0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/books/{}'.format(num))
	book = Book.objects.get(id = num)
	book.title = request.POST['title']
	book.desc = request.POST['desc']
	book.save()
	return redirect('/books/{}'.format(num))

def logout(request):
	del request.session['userid']

	return redirect('/')



























