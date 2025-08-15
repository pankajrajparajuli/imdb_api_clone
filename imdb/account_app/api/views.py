from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegistrationSerializer

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'message': 'User registered successfully'}, status=201)
        return Response(serializer.errors, status=400)
    return Response({'error': 'Method not allowed'}, status=405)

@api_view(['POST,'])
def logout(request):
    if request.method == 'POST':
        request.auth.delete()
        return Response({'message': 'User logged out successfully'}, status=200)
    return Response({'error': 'Method not allowed'}, status=405)