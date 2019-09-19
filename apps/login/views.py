# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect, reverse
from .models import *
from ..belt.models import *


def index(request):
    return render(request, "belt/index.html")

def login_user(request):
    passw_match, user_id = Users.objects.login(request.POST,request)
    print passw_match, user_id
    if passw_match:
        request.session["user_id"] = user_id
        request.session["logged_in"] = True
        return redirect(reverse("dashboard"))
    else:
        print "Failed"
        return redirect(reverse("index"))

def show_user(request, id):
    requested_user_id = int(id)
    users = Users.objects.update_dictionary()
    requested_user = users[requested_user_id]
    books = Reviews.objects.get_by_user(requested_user_id)
    return render(request, "belt/show_user.html",{"users":requested_user,"books":books})

def create_user(request):
    if Users.objects.validate(request.POST,request):
        Users.objects.create_user(request.POST,request)
        return redirect(reverse("index"))
    else: 
        print "Failed"
        return redirect(reverse("index"))

def user_logout_process(request):
    request.session.flush()
    return redirect(reverse("index"))