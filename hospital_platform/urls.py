"""
URL configuration for hospital_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from hospital_app import views
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect


urlpatterns = [
    path('',views.home,name='home'),
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('register/', views.registration, name='register'),
    path('register_view/',views.register_view,name='register_view'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('discharge/<int:id>/', views.discharge, name='discharge'),
    path('make_reservation/', views.make_reservation, name='make_reservation'),
    path('hospital_dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
    path('update_reservation/<int:reservation_id>/<str:action>/', views.update_reservation, name='update_reservation'),
    path('reservation/', views.reservation_status, name='reservation_status'),
    path('', views.redirect_to_login),
    path('logout/', views.logout_view, name='logout'),
    path('Add_Update/<int:hospital>/',views.Add_Update,name='Add_Update'),
    path('Add_Bed/',views.Add_Bed,name='Add_Bed'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
