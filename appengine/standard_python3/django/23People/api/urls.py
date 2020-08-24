from django.urls import path, include

from rest_framework import routers

from . import views


urlpatterns = [
    # ex: /drugs/ List of all drugs
    path('drugs/', views.DrugsList.as_view(), name='drugs_list'), 
    # ex: /drugs/1/ detail of a drug
    path('drugs/<int:pk>/', views.DrugsDetail.as_view(), name='drugs_detail' ),
    # ex: /drug/  create a drug
    path('drug/', views.DrugCreate.as_view(), name='drug_create'),
    # ex: /drug/1/ update or delete a drug
    path('drug/<int:pk>/', views.DrugUpdateDelete.as_view(), name='drug_update_delete' ),
    
    # ex: /vaccination/ List of all vaccination or create a new one
    path('vaccination/', views.VaccinationListCreate.as_view(), name='vaccination_list'), 
    # ex: /vaccination/ List of all vaccination
    path('vaccination/<int:pk>/', views.VaccinationDetailUpdateDelete.as_view(), name='vaccination_detail'), 
    # ex: /register/ Create a new user
    path('register/', views.UserCreate.as_view())
]