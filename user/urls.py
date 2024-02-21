# urls.py
from django.urls import path
from .views import SignUp, SignIn, ForgotPassword, GoogleSignIn
from .views import *

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('signin/', SignIn.as_view(), name='signin'),
    path('forgot-password/', ForgotPassword.as_view(), name="forgot-password"),
    path('signin-with-google/', GoogleSignIn.as_view(), name="signin-with-google")
]

'''
sign in 
{
    "email":
    "passowrd":

}
signup 
{
    "username:"
    "email":
    "passowrd":

}
forgot-password
{
    "email": 
}
'''
