from django.urls import path
from .views import (DoctorDetailsReport, NurseDetailsReport, AddDoctorReportForAllNurse,
                    AddDoctorReport, AddNurseReport, GetNurseReport, GetDoctorReport, AddNurseReportForAllDoctors,
                    DoctorPatientReport, DoctorPatientReportDetail, NursePatientReport, NursePatientReportDetail)

urlpatterns = [

    # Add report by doctor
    path("doctor_report/", AddDoctorReport.as_view(), name="doctor_reports"),

    # Get report by doctor
    path("doctor_report/<int:id>",
         DoctorDetailsReport.as_view(), name="doctor_reports"),

    # Add report by nurse
    path("nurse_report/", AddNurseReport.as_view(), name="nurse_reports"),

    # Get report by nurse
    path("nurse_report/<int:id>", NurseDetailsReport.as_view(), name="nurse_reports"),

    # Get report that nurses added for doctor
    path("doctor_reports/", GetDoctorReport.as_view(), name="doctor_reports"),

    # Get report that doctors added for nurse
    path("nurse_reports/", GetNurseReport.as_view(), name="nurse_reports"),


    # Will Be Removed
    path("<str:pk>/doctor_patient_report/",
         DoctorPatientReport.as_view(), name="patient_report"),

    path("<str:pk>/doctor_patient_report/<int:id>",
         DoctorPatientReportDetail.as_view(), name="patient_report_detail"),

    path("<str:pk>/nurse_patient_report/",
         NursePatientReport.as_view(), name="patient_report"),

    path("<str:pk>/nurse_patient_report/<int:id>",
         NursePatientReportDetail.as_view(), name="patient_report_detail"),

    # Doctor add report for all nurses
    path("add_all_nurses_report",
         AddDoctorReportForAllNurse.as_view(), name="doctor_reports"),

    # Nurse add report for all doctors
    path("add_all_doctors_report",
         AddNurseReportForAllDoctors.as_view(), name="all_doctors_reports"),
]
