# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from .models import *
from ..login.models import *

# Create your views here.
def add(request):
    return render(request, "belt/new_book.html")

def create_book(request):
    book_id = Books.objects.create_validate(request.POST,request) 
    request.session["book_id"] = book_id
    request.session["review"] = request.POST["review"]
    request.session["rating"] = request.POST["rating"]
    return redirect("create_review")

def add_to_session(request):
    request.session["review"] = request.POST["review"]
    request.session["rating"] = request.POST["rating"]
    return redirect("create_review")

def create_reviews(request):
    book_id = int(request.session["book_id"])
    user_id = int(request.session["user_id"])
    book_object = Books.objects.get(id=book_id)
    user_object = Users.objects.get(id=user_id)
    Reviews.objects.create_validate(request.session,book_object,user_object,request)
    return redirect("/books/"+str(book_id))


def dashboard(request):
    reviews = Reviews.objects.three_most_recent()
    books = Books.objects.update_dictionary()
    return render(request, "belt/dashboard.html",{"reviews":reviews,"books":books})

def show_book(request, id):
    book_id = int(id)
    request.session["book_id"] = book_id
    books_dict = Books.objects.update_dictionary()
    requested_book = books_dict[book_id]
    reviews = Reviews.objects.get_by_book(book_id)
    return render(request, "belt/show_book.html",{"books":requested_book, "reviews":reviews})


