from datetime import datetime

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from cars.serializers import DriverDetailSerializer, VehicleDetailSerializer, VehicleDriverSerializer
from cars.models import Driver, Vehicle


class DriverListView(generics.ListAPIView):
    serializer_class = DriverDetailSerializer

    def post(self, request):
        serializer = DriverDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return Response(status=400)

    def get_queryset(self):
        drivers = Driver.objects.all()
        raw_date_gte = self.request.query_params.get('created_at__gte')
        raw_date_lte = self.request.query_params.get('created_at__lte')
        if raw_date_gte is not None:
            date_gte = datetime.strptime(raw_date_gte, '%d-%m-%Y')
            drivers = Driver.objects.filter(created_at__gte=date_gte)
        elif raw_date_lte is not None:
            date_lte = datetime.strptime(raw_date_lte, '%d-%m-%Y')
            drivers = Driver.objects.filter(created_at__lte=date_lte)
        return drivers


class DriverDetailView(APIView):
    def get(self, request, pk):
        try:
            driver = Driver.objects.get(id=pk)
        except Driver.DoesNotExist:
            return Response(status=404)
        serializer = DriverDetailSerializer(driver)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            driver = Driver.objects.get(id=pk)
        except Driver.DoesNotExist:
            return Response(status=404)
        serializer = DriverDetailSerializer(driver, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data=data)
        return Response(status=400)

    def delete(self, request, pk):
        try:
            driver = Driver.objects.get(id=pk)
        except Driver.DoesNotExist:
            return Response(status=404)
        data = {}
        deleting = driver.delete()
        if deleting:
            data["success"] = "deleting successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)


class VehicleListView(generics.ListAPIView):
    serializer_class = VehicleDetailSerializer

    def post(self, request):
        serializer = VehicleDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return Response(status=400)

    def get_queryset(self):
        vehicles = Vehicle.objects.all()
        with_driver = self.request.query_params.get('with_drivers')
        if with_driver == "yes":
            vehicles = Vehicle.objects.filter(driver_id__isnull=False)
        elif with_driver == "no":
            vehicles = Vehicle.objects.filter(driver_id__isnull=True)
        return vehicles


class VehicleDetailView(APIView):
    def get(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(id=pk)
        except Vehicle.DoesNotExist:
            return Response(status=404)
        serializer = VehicleDetailSerializer(vehicle)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(id=pk)
        except Vehicle.DoesNotExist:
            return Response(status=404)
        serializer = VehicleDetailSerializer(vehicle, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data=data)
        return Response(status=400)

    def delete(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(id=pk)
        except Vehicle.DoesNotExist:
            return Response(status=404)
        data = {}
        deleting = vehicle.delete()
        if deleting:
            data["success"] = "deleting successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)


class ChangeDriverView(APIView):
    def post(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(id=pk)
        except Vehicle.DoesNotExist:
            return Response(status=404)
        data_id = request.data["driver_id"]
        if data_id is not None:
            try:
                driver = Driver.objects.get(id=data_id)
            except Driver.DoesNotExist:
                return Response(status=400)
            vehicle.driver_id = driver
        else:
            vehicle.driver_id = data_id
        serializer = VehicleDriverSerializer(vehicle, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data=data, status=201)
        return Response(status=400)
