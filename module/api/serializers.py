from rest_framework import serializers
from module.models import *
# get put update delete Module data
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Module
        fields='__all__'
