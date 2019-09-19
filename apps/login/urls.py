from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main$', views.index, name="index"),
    url(r'^login$', views.login_user, name="login"),
    url(r'^(?P<id>\d+)$', views.show_user, name="show_user"),
    url(r'^create$', views.create_user, name="create_user"),
    url(r'^logout$', views.user_logout_process, name="logout"),
]