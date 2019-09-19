# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
from ..login.models import *
from django.utils.timezone import now

class BooksManager(models.Manager):
    
    def create_validate(self,postData,request):
        "Creates and validates"
        new_title = postData['title']
        new_author = postData['author']
        print postData
        # for book in self.all():
        #     if new_title == book.title:
        #         messages.add_message(request, messages.INFO, "Book already exists")
        # storage = messages.get_messages(request)
        # if storage:
        #     return False
        # else:
        new_book = self.create(title=new_title,author=new_author)
        new_book.save()
        return new_book.id

    def update_dictionary(self):
        books = {}
        for book in self.all():
            books[book.id] = [book.title,book.author,book.id]
        return books


class ReviewsManager(models.Manager):
    reviews = {}
    def create_validate(self,sessionData,book_object,user_object,request):
        "Creates and validates"
        new_reviewer = user_object
        new_book = book_object
        new_desc = sessionData['review']
        new_rating = sessionData['rating']
        # for reviews in self.all().get(book=new_book):
        #     if reviews.reviewer.name == user_object.name:
        #         messages.add_message(request, messages.INFO, "You already have an existing review for ")
        new_review = self.create(desc=new_desc,rating=new_rating,book=new_book,reviewer=new_reviewer)
        new_review.save()
        return new_review.id

    def three_most_recent(self):
        reviews_list = []
        reviews_dict = {}
        i = 0
        for review in self.all().order_by("-created_at"):
            if i < 3:
                i += 1
                reviews_list.append([review.reviewer.name,review.book.title,review.desc,review.rating,review.created_at,review.book.id,review.reviewer.id])
            else:
                break
        return reviews_list

    def get_by_book(self,book_id):
        reviews = []
        book_object = Books.objects.get(id=book_id)
        for review in self.all().filter(book=book_object).order_by("created_at"):
            if review.book.id == book_id:
                reviews.append([review.reviewer.name,review.book.title,review.desc,review.rating, review.created_at,review.reviewer.id])
        return reviews
    
    def get_by_user(self,user_id):
        reviews = []
        user_object = Users.objects.get(id=user_id)
        for review in self.all().filter(reviewer=user_object):
            if review.reviewer.id == user_id:
                reviews.append(review.book.title)
        return reviews

    # def update_dictionary(self):
    #     reviews = {}
    #     for review in self.all():
    #         reviews[review.id] = [review.reviewer.name,review.book.title,review.desc,review.rating]
    #     return reviews

class Books(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    def __repr__(self):
        return "<Books object:{} {} {}>".format(self.id,self.title, self.author)
    objects= BooksManager()


class Reviews(models.Model):
    reviewer = models.ForeignKey(Users, related_name="reviews")
    book = models.ForeignKey(Books, related_name="reviews")
    desc = models.CharField(max_length=50)
    rating = models.IntegerField()
    created_at = models.DateField(default=now)
    def __repr__(self):
        return "<Reviews object:{} {} {} {} {} {}>".format(self.id,self.reviewer, self.book, self.desc, self.rating, self.created_at)
    objects = ReviewsManager()