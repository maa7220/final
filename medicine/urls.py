from django.urls import path
from .views import (MedicinesView, MedicineDetails, AddMedicineAllNurses,
                    AddMedicineNurse, GetMedicineUser, GetMedicineNurse)

urlpatterns = [
    # Medicine
    path('add_medicine', AddMedicineNurse.as_view(), name='medicine_user'),

    path('add_medicine_all_nurses',
         AddMedicineAllNurses.as_view(), name='medicine_nurses'),

    path('medicines', GetMedicineUser.as_view(), name='medicines_user'),

    path('medicines/<str:pk>', GetMedicineUser.as_view(),
         name='medicines_user_details'),

    path('medicines_nurse', GetMedicineNurse.as_view(), name='medicines_nurse'),

    path('', MedicinesView.as_view(), name='medicines'),
    path('<str:pk>', MedicineDetails.as_view(), name='medicine_detail'),
]
