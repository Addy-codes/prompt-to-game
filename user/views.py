from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializers import *
from user.models import *
import json
import firebase


firebaseConfig = settings.FIREBASE_CONFIG
app = firebase.initialize_app(firebaseConfig)
auth = app.auth("./keys/client_secret.json")


class SignIn(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        # print("data: ", data)
        email = data.get('email')
        password = data.get('password')
        try:
            validate_email(email)
        except ValidationError:
            try:
                user = CustomUser.objects.get(username=email)
                # print("user: ", user)
                email = user.email
                # print(f"signin email:{email} from username:{user}: ")
            except CustomUser.DoesNotExist as e:
                return Response({'error': 'Username not found.'}, status=404)
        try:
            user_data = auth.sign_in_with_email_and_password(email, password)
            request.session['localId'] = user_data['localId']
            request.session['idToken'] = user_data['idToken']
        except Exception as e:
            # Handle exceptions (e.g., invalid credentials)
            user_data = {'error': str(e)}
        # Handle user_data (e.g., create Django user session, error handling)
        return Response(user_data)


class SignUp(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        print("Signup data: ", data)
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        print(
            f"==============================================\n{email}: {password}")
        try:
            user_data = auth.create_user_with_email_and_password(
                email, password)
            print("user_data: ", user_data)
            # Handle user_data (e.g., save to database, error handling)
            local_user = CustomUser.objects.create(
                email=email,
                username=username,  # or another unique identifier for your user
                firebase_uid=user_data['localId']  # Store Firebase UID
            )
            request.session['localId'] = user_data['localId']
            request.session['idToken'] = user_data['idToken']

            return Response({
                'message': 'User created successfully',
                'firebase_user': user_data,  # Consider what data you need to return
                'local_user_id': local_user.firebase_uid
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    def get(self, request):
        instances = CustomUser.objects.all()
        serialize = CustomUserSerializer(instances, many=True)
        return Response(serialize.data)


class GoogleSignIn(APIView):
    def post(self, request, *args, **kwargs):
        # Assuming `authenticate_login_with_google` returns the URL for Google's OAuth 2.0 authorization screen
        try:
            auth_url = auth.authenticate_login_with_google()
            return Response({"url": auth_url}, status=200)
        except Exception as e:
            # Handle any errors that occur during the process
            print(e)
            return Response({"error": "Failed to generate Google sign-in URL."}, status=500)


class ForgotPassword(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        email = data.get('email')

        # Validate the email
        try:
            validate_email(email)
        except ValidationError:
            return Response({'error': 'Invalid email format.'}, status=400)

        # Send a password reset email
        try:
            auth.send_password_reset_email(email)
            return Response({'message': 'Password reset email sent.'})
        except Exception as e:
            # Handle exceptions (e.g., email not found in Firebase)
            return Response({'error': str(e)}, status=500)


# firebaseConfig = {
#     "apiKey": "AIzaSyAqNzImdZTgigS2r-Pyevff_tKqPR6n0BY",
#     "authDomain": "chaotix-c07af.firebaseapp.com",
#     "projectId": "chaotix-c07af",
#     "storageBucket": "chaotix-c07af.appspot.com",
#     "messagingSenderId": "422651815888",
#     "appId": "1:422651815888:web:5cd3de69efd3c55aea7bd5",
#     "measurementId": "G-ETVMJ2K42N",
#     "databaseURL": None
# }
