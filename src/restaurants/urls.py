from django.conf.urls import url

from .views import (
    RestaurantListView,
    RestaurantDetailView,
    CreateRestaurantView,
    RestaurantUpdateView
)

urlpatterns = [
    url(r'^$',RestaurantListView.as_view(), name='list'),
    url(r'^create/$',CreateRestaurantView.as_view(), name='create'),
    # url(r'^(?P<slug>[\w-]+)/edit/$',RestaurantUpdateView.as_view(), name='edit'),
    url(r'^(?P<slug>[\w-]+)/$',RestaurantUpdateView.as_view(), name='detail'),    
]