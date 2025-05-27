# jobs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('jobs/<int:pk>/update/', views.job_update, name='job_update'),
    path('jobs/<int:pk>/delete/', views.job_delete, name='job_delete'),
    path('jobs/<int:pk>/apply/', views.apply_for_job, name='apply_for_job'),
    path('jobs/<int:job_pk>/applications/', views.manage_applications, name='manage_applications'),
    path('applications/<int:application_pk>/status/<str:status>/',
         views.update_application_status, name='update_application_status'),

path('applications/<int:pk>/cancel/', views.cancel_application, name='cancel_application'),
    path('jobs/<int:job_pk>/withdraw/', views.withdraw_application, name='withdraw_application'),
]