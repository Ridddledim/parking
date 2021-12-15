from rest_framework import serializers
from cars.models import Driver, Vehicle


class DriverDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)

    class Meta:
        model = Driver
        fields = ("first_name", "last_name", "created_at", "updated_at")



class VehicleDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)

    class Meta:
        model = Vehicle
        fields = "__all__"
        read_only = ("driver_id",)

    def validate_driver_id(self, value):
        """Checks if a driver id was changed"""
        if self.instance and value != self.instance.driver_id:
            raise serializers.ValidationError("A driver_id cannot be changed here.")
        return value

class VehicleDriverSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)

    class Meta:
        model = Vehicle
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(VehicleDriverSerializer, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'driver_id':
                self.fields[field].read_only = True




