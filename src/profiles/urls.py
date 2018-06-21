from .views import profileDetailView
from django.conf.urls import url
urlpatterns = [
    url(r'^(?P<username>[\w-]+)/$', profileDetailView.as_view(), name = 'detail'),
]
