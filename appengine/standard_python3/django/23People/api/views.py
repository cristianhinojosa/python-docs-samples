
from django.contrib.auth.models import User
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics

from .models import Drug, Vaccination
from .serializers import DrugSerializer, VaccinationSerializer, UserSerializer


# Start generic functions

def get_object(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise Http404


# Start Drugs Views

class DrugsList(generics.ListAPIView):
    """
    List all drugs.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = DrugSerializer
    queryset = Drug.objects.all()


class DrugsDetail(generics.RetrieveAPIView):
    """
    Retrieve a drug instance.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = DrugSerializer    
    models = Drug

    def get(self, request, pk, format=None):
        drug = get_object(self.models, pk)
        serializer = self.serializer_class(drug)
        return Response(serializer.data)


class DrugCreate(generics.CreateAPIView):
    """
    Create a new drug.
    """
    serializer_class = DrugSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):

        if not  request.META['CONTENT_TYPE'] == "application/json":
            return Response({'status':400}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DrugUpdateDelete(generics.DestroyAPIView):
    """
    Delete, or Update a drug instance.
    """
    serializer_class = DrugSerializer
    models = Drug
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk, format=None):
        if not  request.META['CONTENT_TYPE'] == "application/json":
            return Response({'status':400}, status=status.HTTP_400_BAD_REQUEST)
        this_object = get_object(self.models, pk)
        serializer = self.serializer_class(this_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk, format=None):
        this_object = get_object(self.models, pk)
        associated_vaccine = Vaccination.objects.filter(drug=this_object.pk)
        if associated_vaccine:
            return Response({"Error":"The drug has an associated vaccine"}, status=status.HTTP_400_BAD_REQUEST)
        this_object.delete()
        return Response({"Message":"The object was deleted"}, status=status.HTTP_204_NO_CONTENT)
    

# Start Vaccination Views

class VaccinationListCreate(generics.ListAPIView, DrugCreate):
    """
    List all Vaccination or create a new one.
    """
    serializer_class = VaccinationSerializer
    queryset = Vaccination.objects.all()



class VaccinationDetailUpdateDelete(DrugUpdateDelete, DrugsDetail):
    """
    Retrieve, update or delete a Vaccination instance.
    """
    serializer_class = VaccinationSerializer    
    models = Vaccination


# Start UserCreate View

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )
