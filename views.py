from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from developers.models import Bank, Developers,project
from rest_framework.decorators import api_view
from .serializers import BankSerializer, DevelopertableSerializer, ManagerSerializer,ProjectSerializer
from rest_framework import status
from rest_framework.decorators import action

# Create your views here.
class developersApiView(APIView):
    serializer_class = DevelopertableSerializer  

    def post(self,request):
        serializer = DevelopertableSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": f"Developer data Posted successfully with ID {Developers.id}"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        developer = Developers.objects.all()
        serializers = DevelopertableSerializer(developer, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class developersDetailsApiView(APIView):
    def get(self,request,pk):
        developer = Developers.objects.get(pk=pk)
        serializer =DevelopertableSerializer(developer)
        print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def patch(self, request, pk):
        try:
            developer = Developers.objects.get(pk=pk)
        except Developers.DoesNotExist:
            return Response({"message": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DevelopertableSerializer(developer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"Developer with id {pk} has been updated."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, pk):
        try:
            developer = Developers.objects.get(pk=pk)
        except Developers.DoesNotExist:
            return Response({"message": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        developer.delete()
        return Response({"message": f"Developer with id {pk} has been deleted."}, status=status.HTTP_204_NO_CONTENT)


class ProjectApiView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            project_data = request.data #postman body
            developers_pk_list = project_data.get('developers', []) 

            project_serializer = ProjectSerializer(data=project_data)

            if project_serializer.is_valid():
                project_instance = project_serializer.save(developers=developers_pk_list)

                project_serializer = ProjectSerializer(project_instance)

                return Response(project_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def get(self, request, *args, **kwargs):
        try:
            projects = project.objects.all()
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProjectUpdateView(APIView):
    def patch(self, request, pk, *args, **kwargs):
        try:
            # Retrieve the existing project instance
            project_instance = project.objects.get(pk=pk)
            
            # Get the data from the request
            project_data = request.data

            developers_pk_list = project_data.get('developers', [])
            project_instance.developers.set(developers_pk_list)

            breakpoint()
            project_serializer = ProjectSerializer(instance=project_instance, data=project_data, partial=True)
            
            if project_serializer.is_valid():

                project_instance = project_serializer.save()

                
                return Response(ProjectSerializer(project_instance).data, status=status.HTTP_200_OK)
            else:
                return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except project.DoesNotExist:
            return Response({"error": f"Project with id {pk} does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ManagerCreateView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Extract data from the request
            manager_data = request.data
            developer_id = manager_data.get('developer')

            # Retrieve the associated Developer instance
            developer = Developers.objects.get(pk=developer_id)

            # Serialize and save Manager instance
            manager_serializer = ManagerSerializer(data=manager_data)
            if manager_serializer.is_valid():
                manager_instance = manager_serializer.save(developer=developer)

                # Update Bank model
                bank_data = {
                    'employee': developer_id, 
                    'employee_salary': manager_data['salary']
                }

                # Serialize and save Bank instance
                bank_serializer = BankSerializer(data=bank_data)
                if bank_serializer.is_valid():
                    bank_instance = bank_serializer.save()

                    # Return successful response with serialized data
                    return Response({
                        'manager': ManagerSerializer(manager_instance).data,
                        'bank': BankSerializer(bank_instance).data
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response(bank_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Return validation errors if Manager serialization fails
                return Response(manager_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Return internal server error if an exception occurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class BankCreateView(APIView):
    def get(self,request):
        bank = Bank.objects.all()
        serializers = BankSerializer(bank, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)