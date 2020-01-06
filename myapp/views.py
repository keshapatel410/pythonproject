import string

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Publisher, Book, Member, Order
from .forms import SearchForm, OrderForm, ReviewForm, MemberForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, hashers
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from random import randint
from django.views.generic import *
import random

from datetime import  datetime


class IndexView(ListView):
    model = Book
    template_name = 'myapp/index.html'


class MyDetailView(DetailView):
    model = Book
    template_name = 'myapp/detail.html'
# def index(request):
#     booklist = Book.objects.all().order_by('id')[:10]
#     return render(request, 'myapp/index.html', {'booklist': booklist})

def about(request):
    # return render(request, 'myapp/about.html')
    lucky_num = request.COOKIES.get('lucky_num')
    if lucky_num is None:
        lucky_num = randint(1, 100)
    resp = render(request, 'myapp/about.html', {'lucky_num': lucky_num})
    resp.set_cookie('lucky_num', lucky_num, max_age=60 * 5)
    return resp


# def details(request, book_id):
#
#     book = get_object_or_404(Book, pk=book_id)
#     return render(request, 'myapp/detail.html', {'book': book})
# Create your views here.

def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            max_price = form.cleaned_data['max_price']

            booklist = Book.objects.filter(price__lte=max_price)

            if category:
                booklist = booklist.filter(category=category)
            return render(request, 'myapp/results.html', {'booklist':booklist, 'name':name, 'category':category})


        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findbooks.html', {'form':form})

def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            books = form.cleaned_data['books']
            order = form.save(commit=False)
            member = order.member
            type = order.order_type
            order.save()
            order.books.set(books)

            if type == 1:
                for b in order.books.all():
                    member.borrowed_books.add(b)
            return render(request, 'myapp/order_response.html', {'books': books, 'order':order})
        else:
            return render(request, 'myapp/placeorder.html', {'form':form})

    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form':form})



def review_view(request):
    member = Member.objects.filter(username=request.user.username).first()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if member.status ==1 or member.status==2:

            if form.is_valid():
                rating = form.cleaned_data['rating']
                book = form.cleaned_data['book']
                if rating > 5 or rating < 1:
                    return HttpResponse('You must enter a rating between 1 and 5!')
                else:
                    review = form.save()
                    book.num_reviews+= 1
                    book.save()
                    return redirect('myapp:index')
            else:
                return render(request, 'myapp/review.html', {'form':form})
        else:
            return render(request, 'myapp/Guest.html', {'error': 'Guest login not allowed ', 'member': member})


    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form':form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = str(datetime.now())
                request.session.set_expiry(60 * 60)
                request.session.save()
                if 'login' not in request.META['HTTP_REFERER']:
                    respLogin = HttpResponseRedirect(request.META['HTTP_REFERER'])
                else:
                    respLogin = HttpResponseRedirect(reverse('myapp:index'))

                return respLogin
                # return HttpResponseRedirect(reverse('myApp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))

def chk_reviews(request, book_id):
    book = Book.objects.get(id=book_id)
    member = Member.objects.filter(username=request.user.username).first()
    if request.user.is_authenticated and member is not None:
        if member.status == 1 or member.status == 2:
            reviews = book.review_set
            rating = reviews.aggregate(Avg('rating'))['rating__avg']
            return render(request, 'myapp/chk_reviews.html', {'rating': rating, 'book': book})
        else:
            return render(request, 'myapp/Guest.html', {'error': 'Guest user cant view reviews ', 'book': book})
    else:
        return render(request, 'myapp/login.html', {'error': 'You are not a registered member!', 'book': book})

def user_register(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.password = hashers.make_password(form.cleaned_data['password'])
            member.save()
            request.session['register_success'] = True
            resp = HttpResponseRedirect(reverse('myapp:user_login'))
            return resp
        else:
            return render(request, 'myapp/register.html', {'form': form})
    else:
        form = MemberForm()
        return render(request, 'myapp/register.html', {'form': form})



def forget(request):
    # if request.user.is_authenticated:
    #     return redirect(reverse('myApp:index'))
    password_reset_not_found = password_reset_success = False
    if request.method == 'POST':
        username = request.POST['username']
        user = User.objects.filter(Q(username=username) or Q(email=username)).first()
        if user:
            letters = string.ascii_lowercase
            password = ''.join(random.choice(letters) for x in range(6))
            user.password = hashers.make_password(password)

            subject = 'PASSWORD RESET REQUEST FORM eBook'
            message = ' PLEASE RESET YOUR PASSWORD ---->' + password
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['keshapatel41096@gmail.com', ]
            send_mail(subject, message, email_from, recipient_list)

            user.save()

            # password_reset_success = True
        else:
            return HttpResponse('USER NOT FOUND !')
        request.session.save()
        return render(request, 'myapp/Emailsent.html', )

    else:
        return render(request, 'myapp/Forgot.html')

z