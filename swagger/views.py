from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializer import UserRegisterationSerializer,UserLoginSerializer,UserProfileSerializer,DoctorProfileSerializer
from django.contrib.auth import authenticate
from .tokens import get_tokens_for_user
from rest_framework.permissions import IsAuthenticated
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

class UserRegisterationView(APIView):
     def get(self,request,format=None):
          return Response({
               'msg':'Register Your Credentials',
               'Fields':['first_name','last_name','email','username','password','password2']
          },status=status.HTTP_200_OK)
     
     def post(self,request,format=None):
          serializer = UserRegisterationSerializer(data=request.data)
          if serializer.is_valid():
               user = serializer.save()
               return Response({'msg':'Registeration Successfull'},status=status.HTTP_201_CREATED)
          return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
     
     def post(self,request,format=None):
          serializer = UserLoginSerializer(data=request.data) 
          if serializer.is_valid():
               email = serializer.data.get('email') 
               password = serializer.data.get('password')
               user=authenticate(request,email=email,password=password)
               if user is not None:
                    if not user.blocked:
                         token = get_tokens_for_user(user)
                    else:
                         return Response({"msg":"Your Account is blocked"})
                    return Response({"msg":"Login Success","token":token},status=status.HTTP_200_OK)
               else:
                    return Response({'errors':{'non_field_errors':['Email or Password is not valid']}},status=status.HTTP_404_NOT_FOUND)
          return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
          
               
class UserProfileView(APIView):
     permission_classes = [IsAuthenticated]
     def get(self,request,format=None):
          serializer = UserProfileSerializer(request.user)
          return Response(serializer.data,status=status.HTTP_200_OK)
     
     def put(self,request,format=None):
          
          user = request.user
          if user.is_doctor:
               serializer = DoctorProfileSerializer(user,data=request.data,partial=True)
          else:
               serializer = UserProfileSerializer(user,data=request.data,partial=True)
          if serializer.is_valid():
               serializer.save()
               return Response({'msg':'Complete Data Updated'})
          return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
     
     
     def delete(self,request,format=None):
          
          user = request.user
          user.delete()
          return Response({'msg':'Data Deleted'},status=status.HTTP_200_OK)
     
class BlockAPIView(APIView):
    def patch(self, request,id):
        try:
            user = User.objects.get(id=id)  # Check if the user exists
        except User.DoesNotExist:
            return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        action = request.query_params.get('action', None)
        if action not in ['block', 'unblock']:
            return Response({"detail": "Invalid action. Use 'block' or 'unblock' as the query parameter."}, status=status.HTTP_400_BAD_REQUEST)

        if action == 'block':
            user.blocked = True
            user.save()
            return Response({"detail": "User blocked."}, status=status.HTTP_200_OK)
        elif action == 'unblock':
            user.blocked = False

        user.save()

        return Response({"detail": "User Unblocked."}, status=status.HTTP_200_OK)


          
class HomePageView(APIView):
     permission_classes = [IsAuthenticated]
     def get(self,request,format=None):

          user = User.objects.get(email=request.user)
          if not user.is_doctor and not user.is_admin:                      # For User
               users = User.objects.filter(is_doctor=True)
               serializer = DoctorProfileSerializer(users,many=True)
               return Response(serializer.data,status=status.HTTP_200_OK)
          if user.is_doctor: 
               doctors = User.objects.filter(is_doctor=True)                                               # For Doctor
               serializer = DoctorProfileSerializer(doctors,many=True)
               return Response(serializer.data,status=status.HTTP_200_OK)
          
               
         
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"detail": "Refresh token not provided."},status=status.HTTP_400_BAD_REQUEST)
            try:
                token = RefreshToken(refresh_token)
                
                # token.blacklist()
            except Exception as e:
                  return Response({"detail": "Invalid refresh token."},status=status.HTTP_400_BAD_REQUEST)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
        except Exception as e:
             return Response({"detail": "An error occurred while processing the request."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
