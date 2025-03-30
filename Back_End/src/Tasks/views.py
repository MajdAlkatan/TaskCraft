from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import TaskSerializer
# from MAROUF WORKSPACE.models import user_workspace 

@api_view(['POST'])
def create_task(request):
    
    # user = user_workspace.objects.get(request.user_id)
    # if user.role == "owner" & user.role == "partner":

        serializer = TaskSerializer(data = request.data)
        if serializer.is_valid():
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        
    # else:
    #     return Response("No Add Permissions " , status = status.HTTP_400_BAD_REQUEST)


