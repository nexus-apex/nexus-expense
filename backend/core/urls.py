from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/create/', views.expense_create, name='expense_create'),
    path('expenses/<int:pk>/edit/', views.expense_edit, name='expense_edit'),
    path('expenses/<int:pk>/delete/', views.expense_delete, name='expense_delete'),
    path('expensecategories/', views.expensecategory_list, name='expensecategory_list'),
    path('expensecategories/create/', views.expensecategory_create, name='expensecategory_create'),
    path('expensecategories/<int:pk>/edit/', views.expensecategory_edit, name='expensecategory_edit'),
    path('expensecategories/<int:pk>/delete/', views.expensecategory_delete, name='expensecategory_delete'),
    path('expensereports/', views.expensereport_list, name='expensereport_list'),
    path('expensereports/create/', views.expensereport_create, name='expensereport_create'),
    path('expensereports/<int:pk>/edit/', views.expensereport_edit, name='expensereport_edit'),
    path('expensereports/<int:pk>/delete/', views.expensereport_delete, name='expensereport_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
