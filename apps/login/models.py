# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt
from django.utils.timezone import now
from datetime import datetime 


class UsersManager(models.Manager):
    def login(self,postData,request):
        print postData
        "loops through all the users in the database and checks if the username mathces the password and result variable is True if they match"
        reg_email = postData["email"]
        reg_raw_passw = str(postData["passw"])
        user_id = "None"
        for user in self.all():
            if user.email == reg_email:
                if bcrypt.checkpw(reg_raw_passw.encode(), user.password.encode()):
                    result = True
                    user_id = int(user.id)
                    break
                else:
                    result = False
            else:
                result = False
        if not result:
            messages.add_message(request, messages.WARNING, "Username doesn't exist or password doesn't match")
        return (result, user_id)

    def create_user(self,postData,request):
        "Creates a new user and returns the id of the newly created user"
        new_name = postData['name']
        new_alias = postData['alias']
        raw_passw = postData['passw']
        new_email = postData['email']
        new_passw = bcrypt.hashpw(raw_passw.encode(), bcrypt.gensalt())
        new_user = self.create(name=new_name,alias=new_alias,email=new_email,password=new_passw)
        new_user.save()
        return new_user.id

    def validate(self,postData,request):
        "Validates"
        new_name = postData['name']
        new_alias = postData['alias']
        passw = postData['passw']
        confirm_passw = postData['confirm_passw']
       
        if passw != confirm_passw:
            messages.add_message(request, messages.INFO, "Passwords do not match")
        if len(passw) < 8:
            messages.add_message(request, messages.INFO, "Password cannot be less than 8 characters")
        if len(new_alias) < 3:
            messages.add_message(request, messages.INFO, "Username has to at least 3 characters")
        if len(new_name) < 3:
            messages.add_message(request, messages.INFO, "Name has to be at least 3 characters")
        for user in self.all():
            if new_name == user.name:
                messages.add_message(request, messages.INFO, "Name already exists")
            if new_alias == user.alias:
                messages.add_message(request, messages.INFO, "Username already exists")
            if new_name == user.password:
                messages.add_message(request, messages.INFO, "Pasword already exists")
        storage = messages.get_messages(request)
        if storage:
            return False
        else:
            return True

    def update_dictionary(self):
        """
        Creates a dictionary of all the user items that can be accessed via the user.id; 
        Used to pass along info of logged in user to the template in dashboard.html
        """
        users = {}
        for user in self.all():
            users[user.id] = [user.name,user.alias,user.email]
        return users

class Users(models.Model):
    
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50,default="1234")
    def __repr__(self):
        return "<Users object:{} {} {} {} {}>".format(self.id, self.name, self.alias, self.email, self.password)

    objects= UsersManager()

