from django.urls import path
from . import views
from .views import listBooks, processOption, listOnLoan, listDueToday, listAvailable, borrowBook, index, loginView, signupView, logoutView

urlpatterns = [
    path('books/', listBooks, name='listBooks'),
    path('process_option/', processOption, name='processOption'),
    path('loans/', listOnLoan, name='listOnLoan'),
    path('dueToday/', listDueToday, name='listDueToday'),
    path('listAvailable/', listAvailable, name='listAvailable'),
    path('borrowBook/', borrowBook, name='borrowBook'),
    path('', index, name='home'),
    path('login', loginView, name='loginView'),
    path('signup',signupView, name='signupView'),
    path('logout', logoutView, name='logoutView')
]
