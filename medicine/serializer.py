from rest_framework import serializers
from .models import Medicines, Medicine
from users.models import Nurse, Doctor
from rest_framework.validators import ValidationError


class MedicinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicines
        fields = ['id', 'name', 'created', 'updated']


# Add to Nurse
class AddMedicineSerializer(serializers.ModelSerializer):
    nurse = serializers.SlugRelatedField(
        slug_field="user_id", queryset=Nurse.objects.all(), many=True)

    class Meta:
        model = Medicine
        fields = '__all__'


class ResultMedicineSerializer(serializers.ModelSerializer):
    nurse = serializers.SerializerMethodField(source='get_nurse')
    patient = serializers.StringRelatedField()
    name = serializers.StringRelatedField()

    class Meta:
        model = Medicine
        exclude = ('doctor', )

    @staticmethod
    def get_nurse(obj):
        nurse_list = []
        nurse = obj.nurse.all()
        for i in nurse:
            data = i.user
            nurse_list.append({"id": data.id, "name": data.name, })
        return nurse_list


class SimpleResultMedicineSerializer(serializers.ModelSerializer):
    nurse = serializers.StringRelatedField()
    patient = serializers.StringRelatedField()
    name = serializers.StringRelatedField()

    class Meta:
        model = Medicine
        fields = '__all__'


class NurseResultMedicineSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField()
    patient = serializers.StringRelatedField()
    name = serializers.StringRelatedField()

    class Meta:
        model = Medicine
        exclude = ('nurse', )


# -------  Add Medicines for all Nurses
class AddAllNursesMedicineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medicine
        exclude = ('nurse', )
