from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
from .models import Book
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.login_validator(request.POST)
    print(request.POST)
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    print(pw_hash)
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pw_hash)

        request.session['userid'] = user.id
        return redirect('/books')
            
    return redirect('/')

def login(request):
        user = User.objects.filter(email = request.POST['email'])
        print(user)
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                return redirect('/books')
            else:
                messages.error(request, "Email/password is incorrect.")
        else:
            messages.error(request, "Email isnt registered yet.")
        return redirect('/')
def books(request):
    context = {
        'allbooks' : Book.objects.all(),
        'theuser' : User.objects.get(id = request.session['userid'])
    }
    return render(request,'books.html',context)

def create_book(request):
    book = Book.objects.create(
        title = request.POST['title'],
        desc = request.POST['desc-text'],
        uploaded_by = User.objects.get(id = request.session['userid'])
    )
    
    return redirect(f'/books/{book.id}')

def edit_book(request,id):
    context = {
        'editbook' : Book.objects.get(id = id),
        'wholeuser' : User.objects.get(id= request.session['userid']
        )}
    return render(request,'viewbook.html',context)


def update_book(request,id):
    c = Book.objects.get(id =id)
    c.desc = request.POST['edit_desc']
    c.save()
    return redirect(f'/books/{id}')
    
def fav_book(request,id):
    this_book = Book.objects.get(id=id)
    this_user = User.objects.get(id= request.session['userid'])
    this_user.fav_book.add(this_book)
    return redirect (f'/books/{id}')

def unfav_book(request, id):
    this_book = Book.objects.get(id=id)
    this_user = User.objects.get(id= request.session['userid'])
    this_user.fav_book.remove(this_book)
    return redirect (f'/books/{id}')

def logout(request):
    request.session.clear()
    return redirect('/')
