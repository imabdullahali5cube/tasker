from rest_framework import serializers
from .models import Developers, project,Manager,Bank

class DevelopertableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developers
        fields = ['id','name','phone_num','Email']

class ProjectSerializer(serializers.ModelSerializer):
    # developer_id = serializers.ReadOnlyField()
    developers = DevelopertableSerializer(many=True,read_only=True)

    class Meta:
        model = project
        fields = ['id','project_name','developers']

class ManagerSerializer(serializers.ModelSerializer):
    developer = DevelopertableSerializer(read_only=True)

    class Meta:
        model = Manager
        fields = '__all__'

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'