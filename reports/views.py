from rest_framework import generics, views
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from .models import DoctorReport, NurseReport
from .serializer import (
    ReportNursePatientSerializer, DoctorReportAllNursesSerializer, ResultNurseReportAddedDoctorSerializer,
    ResultDoctorReportAddedNurseSerializer, NurseReportAllDoctorsSerializer,
    DoctorReportSerializer, ReportDoctorPatientSerializer,
    ResultDoctorReportSerializer, NurseReportSerializer, ResultNurseReportSerializer)
from rest_framework.permissions import IsAuthenticated
from users.models import Nurse, Patient, Doctor
from users.permissions import IsDoctor, IsNurse


# ======================= Doctor =======================================
class AddDoctorReport(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsDoctor]
    serializer_class = DoctorReportSerializer

    def post(self, serializer):
        data = self.request.data
        doctor = Doctor.objects.get(user=self.request.user)
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            result = serializer.save(added_by=doctor)
            response = {
                "report": ResultDoctorReportSerializer(result, context=self.get_serializer_context()).data,
                "message": "Report Created successfully",
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

    def get(self, request):
        user = request.user
        current_doctor = Doctor.objects.get(user=user)
        report = current_doctor.doctor_reports.all()
        serializer = ResultDoctorReportSerializer(report, many=True)

        return Response({"result": report.count(), 'reports': serializer.data})


class DoctorDetailsReport(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsDoctor]
    serializer_class = DoctorReportSerializer

    def get(self, request, id=None):
        try:
            report = DoctorReport.objects.get(id=id)
            serializer = ResultDoctorReportSerializer(report)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Report Not Found"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        try:
            report = DoctorReport.objects.get(id=id)
            doctor = Doctor.objects.get(user=self.request.user)
            data = request.data
            serializer = self.serializer_class(instance=report, data=data)

            serializer.is_valid(raise_exception=True)
            result = serializer.save(added_by=doctor)
            response = {
                "message": "Report Updated successfully",
                "data": ResultDoctorReportSerializer(result).data,
            }
            return Response(data=response, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({"message": "Report Not Found"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        try:
            report = DoctorReport.objects.get(id=id)
            report.delete()
            return Response({"message": "Report Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"message": "Report Not Found"}, status=status.HTTP_400_BAD_REQUEST)


# Return Report For Doctor (That Nurse added for him)
class GetDoctorReport(views.APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request, id=None):
        try:
            user = request.user
            if id:
                report = NurseReport.objects.get(id=id)
                serializer = ResultDoctorReportAddedNurseSerializer(report)
                return Response({"report": serializer.data}, status=status.HTTP_200_OK)

            else:
                current_doctor = Doctor.objects.get(user_id=user)
                report = current_doctor.doctors_reports.all()

                serializer = ResultDoctorReportAddedNurseSerializer(
                    report, many=True)
                return Response({'result': len(serializer.data), "reports": serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Report does not exist"}, status=status.HTTP_400_BAD_REQUEST)

# ======================= Nurse =======================================


class AddNurseReport(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsNurse]
    serializer_class = NurseReportSerializer

    def post(self, serializer):
        data = self.request.data
        nurse = Nurse.objects.get(user=self.request.user)
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            result = serializer.save(added_by=nurse)
            response = {
                "report": ResultNurseReportSerializer(result, context=self.get_serializer_context()).data,
                "message": "Report Created successfully",
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

    def get(self, request):
        user = request.user
        current_nurse = Nurse.objects.get(user=user)
        report = current_nurse.nurses_reports.all()
        serializer = ResultNurseReportSerializer(report, many=True)

        return Response({"result": report.count(), 'reports': serializer.data})


class NurseDetailsReport(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsNurse]
    serializer_class = NurseReportSerializer

    def get(self, request, id=None):
        try:
            report = NurseReport.objects.get(id=id)
            serializer = ResultNurseReportSerializer(report)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Report Not Found"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        try:
            report = NurseReport.objects.get(id=id)
            nurse = Nurse.objects.get(user=self.request.user)
            data = request.data
            serializer = self.serializer_class(instance=report, data=data)

            serializer.is_valid(raise_exception=True)
            result = serializer.save(added_by=nurse)
            response = {
                "message": "Report Updated successfully",
                "data": ResultNurseReportSerializer(result).data,
            }
            return Response(data=response, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Report Not Found"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        try:
            report = NurseReport.objects.get(id=id)
            report.delete()
            return Response({"message": "Report Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"message": "Report Not Found"}, status=status.HTTP_400_BAD_REQUEST)


# Return Report For Nurse (That Doctor added for her)
class GetNurseReport(views.APIView):
    permission_classes = [IsAuthenticated, IsNurse]

    def get(self, request, id=None):
        try:
            user = request.user
            if id:
                report = DoctorReport.objects.get(id=id)
                serializer = ResultNurseReportAddedDoctorSerializer(report)
                return Response({"report": serializer.data}, status=status.HTTP_200_OK)

            else:
                current_nurse = Nurse.objects.get(user_id=user)
                report = current_nurse.nurse_reports.all()

                serializer = ResultNurseReportAddedDoctorSerializer(
                    report, many=True)
                return Response({'result': len(serializer.data), "reports": serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Report does not exist"}, status=status.HTTP_400_BAD_REQUEST)


# ======================= Return & Add Report For patient =======================================
class DoctorPatientReport(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReportDoctorPatientSerializer

    def post(self, serializer, pk=None):
        data = self.request.data
        doctor = Doctor.objects.get(user=self.request.user)
        serializer = self.serializer_class(data=data)

        if data['patient'] == pk:
            if serializer.is_valid(raise_exception=True):
                result = serializer.save(added_by=doctor)
                response = {
                    "report": ResultDoctorReportSerializer(result, context=self.get_serializer_context()).data,
                    "message": "Report Created successfully",
                }

                return Response(data=response, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        else:
            return Response({'ID of patient not equal in the body'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        doctor = Doctor.objects.get(user=self.request.user)
        patient = Patient.objects.get(pk=pk)
        reports = patient.patient_reports.filter(added_by=doctor)
        serializer = ResultDoctorReportSerializer(reports, many=True)
        return Response({'result': len(serializer.data), "reports": serializer.data}, status=status.HTTP_200_OK)


class DoctorPatientReportDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReportDoctorPatientSerializer

    def get(self, request, pk=None, id=None):
        report = DoctorReport.objects.get(id=id)
        serializer = ResultDoctorReportSerializer(report)
        return Response({"report": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request,  pk=None, id=None):
        report = DoctorReport.objects.get(id=id)
        patient = Patient.objects.get(id=pk)

        data = request.data
        data['patient'] = patient.id

        serializer = self.serializer_class(
            instance=report, data=data,)

        if serializer.is_valid(raise_exception=True):
            result = serializer.save()
            response = {
                "message": "Report Updated successfully",
                "data": ResultDoctorReportSerializer(result).data,
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)

    def delete(self, request, id=None, pk=None):
        report = DoctorReport.objects.get(id=id)
        report.delete()
        return Response({"reports": 'Report Deleted Successfully'}, status=status.HTTP_200_OK)


class NursePatientReport(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReportNursePatientSerializer

    def post(self, serializer, pk=None):
        data = self.request.data
        nurse = Nurse.objects.get(user=self.request.user)
        serializer = self.serializer_class(data=data)

        if data['patient'] == pk:
            if serializer.is_valid(raise_exception=True):
                result = serializer.save(added_by=nurse)
                response = {
                    "report": ResultNurseReportSerializer(result, context=self.get_serializer_context()).data,
                    "message": "Report Created successfully",
                }

                return Response(data=response, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({'ID of patient not equal in the body'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        nurse = Nurse.objects.get(user=self.request.user)
        patient = Patient.objects.get(pk=pk)
        reports = patient.patients_reports.filter(added_by=nurse)
        serializer = ResultNurseReportSerializer(reports, many=True)
        return Response({'result': len(serializer.data), "reports": serializer.data}, status=status.HTTP_200_OK)


class NursePatientReportDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReportNursePatientSerializer

    def get(self, request, pk=None, id=None):
        try:
            report = NurseReport.objects.get(id=id)
            serializer = ResultNurseReportSerializer(report)
            return Response({"report": serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Report does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,  pk=None, id=None):
        try:
            report = NurseReport.objects.get(id=id)
            patient = Patient.objects.get(id=pk)

            data = request.data
            data['patient'] = patient.id

            serializer = self.serializer_class(
                instance=report, data=data,)

            serializer.is_valid(raise_exception=True)
            result = serializer.save()
            response = {
                "message": "Report Updated successfully",
                "data": ResultNurseReportSerializer(result).data,
            }
            return Response(data=response, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Report does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None, pk=None):
        report = DoctorReport.objects.get(id=id)
        report.delete()
        return Response({"reports": 'Report Deleted Successfully'}, status=status.HTTP_200_OK)


# ========== AddDoctorReportForAllNurse ===========
class AddDoctorReportForAllNurse(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DoctorReportAllNursesSerializer

    def post(self, serializer, pk=None):
        data = self.request.data
        doctor = Doctor.objects.get(user=self.request.user)
        patient = Patient.objects.get(id=data.get('patient'))
        nurses = patient.nurse.all()

        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            result = serializer.save(added_by=doctor, nurse=nurses)
            response = {
                "report": ResultDoctorReportSerializer(result, context=self.get_serializer_context()).data,
                "message": "Report Created successfully",
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            return Response(data={serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# ========== AddNurseReportForAllDoctors ===========
class AddNurseReportForAllDoctors(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NurseReportAllDoctorsSerializer

    def post(self, serializer, pk=None):
        data = self.request.data
        nurse = Nurse.objects.get(user=self.request.user)
        patient = Patient.objects.get(id=data['patient'])
        doctors = patient.doctor.all()

        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            result = serializer.save(added_by=nurse, doctor=doctors)
            response = {
                "report": ResultNurseReportSerializer(result, context=self.get_serializer_context()).data,
                "message": "Report Created successfully",
            }

        return Response(data=response, status=status.HTTP_201_CREATED)
