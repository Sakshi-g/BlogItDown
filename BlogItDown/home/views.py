from django.shortcuts import render , redirect
from .form import *
from django.contrib.auth import logout
import requests
import random
import time
import json
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
from webdriver_manager.chrome import ChromeDriverManager



def logout_view(request):
    logout(request)
    return redirect('/')

def books(request):
    def get_books():
        r = requests.get('https://www.goodreads.com/list/show/9440.100_Best_Books_of_All_Time_The_World_Library_List')
        soup = BeautifulSoup(r.text, 'html.parser')
        booklist = soup.find_all('a', {'class': 'bookTitle'})
        with open('all_books.txt', 'w') as f:
            for book in booklist:
                f.write(book['href']+'\n')

    def get_book_data():
        with open('all_books.txt') as f:
            bookList = f.readlines()
        all_data = []

        for idx, book in enumerate(bookList):

            if(idx < 10):
                print(f'Extracting data for book {idx+1}')
                r = requests.get('https://www.goodreads.com/'+ book)
                soup = BeautifulSoup(r.text, 'html.parser')
                images = soup.find_all('img', {'id': 'coverImage'})

                for item in images:

                    data = {
                        'title': soup.find('h1', {'id':'bookTitle'}).text,
                        'author':soup.find('span', {'itemprop':'name'}).text,
                        'ratings': soup.find('span', {'itemprop':'ratingValue'}).text,
                        'genre': soup.find('a', {'class':'actionLinkLite bookPageGenreLink'}).text,
                        'image': item['src']

                          }
                    all_data.append(data)

        return all_data

    list_books = get_book_data()
    context = {'books' : list_books}
    print(context['books'][0]['title'])
    return render(request , 'books.html' , context)

def home(request):
    print("blog")

    #Final quotes
    url1 = "https://bodybuilding-quotes1.p.rapidapi.com/quotes"
    querystring = {"page": str(random.randint(0,10))}

    headers = {
        'x-rapidapi-host': "bodybuilding-quotes1.p.rapidapi.com",
        'x-rapidapi-key': "2f224af47cmsh4e1d91d655012e3p1945bcjsn5abe5e2783a5"
        }

    response1 = requests.request("GET", url1, headers=headers, params=querystring)
    n1 = json.loads(response1.text)

    #print(response.text)

    #Final jokes
    url2 = "https://dad-jokes.p.rapidapi.com/random/joke"

    headers = {
        'x-rapidapi-host': "dad-jokes.p.rapidapi.com",
        'x-rapidapi-key': "2f224af47cmsh4e1d91d655012e3p1945bcjsn5abe5e2783a5"
        }

    response2 = requests.request("GET", url2, headers=headers).json()
    print(response2)

    #context = {'blogs' : BlogModel.objects.all(), 'resp': response, 'setup': response['body'][0]['setup'] ,'punchline':response['body'][0]['punchline']}

    url3 = "https://indian-news-live.p.rapidapi.com/news/cricket"

    querystring = {"page": str(random.randint(0,10))}
    headers = {
        'x-rapidapi-host': "indian-news-live.p.rapidapi.com",
        'x-rapidapi-key': "2f224af47cmsh4e1d91d655012e3p1945bcjsn5abe5e2783a5"
        }


    response3 = requests.request("GET", url3, headers=headers, params=querystring)
    n = json.loads(response3.text)

    print(random.choice(n))
    context = {'blogs' : BlogModel.objects.all(), 'thought': random.choice(n1), 'resp' : random.choice(n), 'setup': response2['body'][0]['setup'] ,'punchline':response2['body'][0]['punchline']}
    return render(request , 'home.html' , context)



def login_view(request):
    return render(request , 'login.html')

def blog_detail(request , slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug = slug).first()
        context['blog_obj'] =  blog_obj
    except Exception as e:
        print(e)
    return render(request , 'blog_detail.html' , context)


def see_blog(request):
    context = {}

    try:
        blog_objs = BlogModel.objects.filter(user = request.user)
        context['blog_objs'] =  blog_objs
    except Exception as e:
        print(e)

    print(context)
    return render(request , 'see_blog.html' ,context)


def add_blog(request):
    context = {'form' : BlogForm}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']

            blog_obj = BlogModel.objects.create(
                user = user , title = title,
                content = content, image = image
            )
            print(blog_obj)
            return redirect('/add-blog/')



    except Exception as e :
        print(e)

    return render(request , 'add_blog.html' , context)


def blog_update(request , slug):
    context = {}
    try:

        blog_obj = BlogModel.objects.get(slug = slug)
        if blog_obj.user != request.user:

            return redirect('/')

        initial_dict = {'content': blog_obj.content}
        form = BlogForm(initial = initial_dict)
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']

            blog_obj = BlogModel.objects.create(
                user = user , title = title,
                content = content, image = image
            )


        context['blog_obj'] = blog_obj
        context['form'] = form
    except Exception as e :
        print(e)

    return render(request , 'update_blog.html' , context)

def blog_delete(request , id):
    try:
        blog_obj = BlogModel.objects.get(id = id)

        if blog_obj.user == request.user:
            blog_obj.delete()

    except Exception as e :
        print(e)

    return redirect('/see-blog/')


def  register_view(request):
    return render(request , 'register.html')



def verify(request,token):
    try:
        profile_obj = Profile.objects.filter(token = token).first()

        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
        return redirect('/login/')

    except Exception as e :
        print(e)

    return redirect('/')
