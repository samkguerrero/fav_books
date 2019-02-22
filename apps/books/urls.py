from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'(?P<book_id>[0-9]+)$', views.books),
    url(r'add_book$', views.add_book),
    url(r'user_fav_a_book$', views.user_fav_a_book),
    url(r'user_update_book$', views.user_update_book),
    url(r'user_delete_book$', views.user_delete_book),
    url(r'user_un_fav_book$', views.user_un_fav_book),
]