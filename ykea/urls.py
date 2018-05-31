from django.conf.urls import url, include
from django.contrib.auth.views import login, logout
from rest_framework import routers
from ykea import views

listOfAddresses = ["sd2018-ykea-b2", "d2018-ykeab6", "sd2018-ykeab7-2","sd2018-ykeab8", "sd2018-ykeab9"]
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^items/$', views.items, name='items'),
    url(r'^items/(?P<category>.*)/$', views.items, name='items'),
    url(r'^item/(?P<item_number>.*)/$', views.item, name='item'),
    url(r'^shoppingcart/$', views.shoppingcart, name='shoppingcart'),
    url(r'^buy/$', views.buy, name='buy'),
    url(r'^process_cart/$', views.process_cart, name='process_cart'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^comparator/$', views.comparator, {'ips': listOfAddresses}, name='comparator'),
]