from django.conf.urls import url, include
from django.contrib.auth.views import login, logout
from rest_framework import routers
from ykea import views

router = routers.DefaultRouter()
router.register(r'items', views.ItemViewSet)

listOfAddresses = ['127.0.0.1:8000', '127.0.0.1:8000']

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^items/$', views.items, name='items'),
    url(r'^items/(?P<category>.*)/$', views.items, name='items'),
    url(r'^item/(?P<item_number>.*)/$', views.item, name='item'),
    url(r'^shoppingcart/$', views.shoppingcart, name='shoppingcart'),
    url(r'^buy/$', views.buy, name='buy'),
    url(r'^process_cart/$', views.process_cart, name='process_cart'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^accounts/login/$',  login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^comparator/$', views.comparator, {'ips': listOfAddresses}, name='comparator'),
]