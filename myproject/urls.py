"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myproject import views
urlpatterns = [
    path('', views.Home , name='Home'),
    path('c/', views.comingSoon , name='comingSoon'),
    path('admin', admin.site.urls),
    path('signup/', views.signup , name='signup'),
    path('tsignup/', views.tsignup , name='tsignup'),
    path('signin/', views.signin , name='signin'),
    path('tsignin/', views.tsignin , name='tsignin'),
    path('srequest/', views.srequest , name='srequest'),
    path('trackstat/', views.trackstat , name='trackstat'),
    path('showstatus/', views.showstatus , name='showstatus'),
    path('request_list/', views.request_list , name='request_list'),
    path('approve_request/<slug:request_id>/', views.approve_request , name='approve_request'),
    path('reject_request/<slug:request_id>/', views.reject_request , name='reject_request'),
]
