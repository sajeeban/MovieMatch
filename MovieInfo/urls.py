from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^result/$', views.search, name="search"),
    url(r'^register/$', views.UserFormView.as_view(), name="register"),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
]

