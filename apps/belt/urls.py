from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^dashboard$', views.dashboard, name="dashboard"),
    url(r'^add$', views.add, name="add_book"),
    url(r'^create$', views.create_book, name="create_book"),
    url(r'^create/reviews$', views.create_reviews,name="create_review"),
    url(r'^add/reviews$', views.add_to_session,name="add_review"),
    url(r'^(?P<id>\d+)$', views.show_book,name="show_book")
]