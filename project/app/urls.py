from django.urls import path
from . import views

urlpatterns = [
    path('donor/register/', views.donor_register, name='donor_register'),
    path('staff/register/', views.staff_register, name='staff_register'),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('donorhome/', views.donor_home, name='donor_home'),
    path('staffhome/', views.staff_home, name='staff_home'),
    path('addchild/', views.addchild, name='addchild'),
    path('viewchild/', views.viewchild, name='viewchild'),
    path('editchild/<int:id>/', views.editchild, name='editchild'),
    path('deletechild/<int:id>/', views.deletechild, name='deletechild'),
    path('stafprofile/', views.stafprofile, name='stafprofile'),
    path('updatestafprofile/', views.updatestafprofile, name='updatestafprofile'),
]

    

