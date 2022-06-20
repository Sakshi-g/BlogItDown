from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile
from .helpers import *
from rest_framework import authentication, permissions
from django.contrib.auth import authenticate , login
from rest_framework.permissions import IsAuthenticated


class HelloView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)



class LoginView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    http_method_names = ['get', 'head', 'delete', 'post', 'put' ,'patch']
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        usernames = [user.username for user in User.objects.all()]
        passwords = [user.password for user in User.objects.all()]
        fin = [usernames, passwords]
        return Response(fin)

    def delete(self, request):

        data = request.data

        check_user = User.objects.filter(username = data.get('username')).first()
        if check_user is None:
            return Response({"error: user not found"})


        check_user.delete()

        return Response({"result":"User deleted"})

    def patch(self, request):

        response = {}
        response['status'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data

            if data.get('username') is None:
                response['message'] = 'key username not found'
                raise Exception('key username not found')

            if data.get('password') is None:
                response['message'] = 'key password not found'
                raise Exception('key password not found')


            check_user = User.objects.filter(username = data.get('username')).first()

            if check_user:
                #check_user = User.objects.filter(username = data.get('username')).first()
                check_user.delete()
                response['message'] = 'username  already taken'
                #raise Exception('username  already taken')
                user_obj = User.objects.create(email = data.get('username') , username = data.get('username'))
                user_obj.set_password(data.get('password'))
                user_obj.save()
                token = generate_random_string(20)
                Profile.objects.create(user = user_obj , token = token)

                #send_mail_to_user(token , data.get('username'))
                response['message'] = 'User Updated'
                response['status'] = 200

            user_obj = User.objects.create(email = data.get('username') , username = data.get('username'))
            user_obj.set_password(data.get('password'))
            user_obj.save()
            token = generate_random_string(20)
            Profile.objects.create(user = user_obj , token = token)

            #send_mail_to_user(token , data.get('username'))
            response['message'] = 'User Updated'
            response['status'] = 200



        except Exception as e :
            print(e)

        return Response(response)





    def post(self , request):
        response = {}
        response['status'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data

            if data.get('username') is None:
                response['message'] = 'key username not found'
                raise Exception('key username not found')

            if data.get('password') is None:
                response['message'] = 'key password not found'
                raise Exception('key password not found')


            check_user = User.objects.filter(username = data.get('username')).first()

            if check_user is None:
                response['message'] = 'invalid username , user not found'
                raise Exception('invalid username not found')


            user_obj = authenticate(username = data.get('username') , password = data.get('password'))
            if user_obj:
                login(request, user_obj)
                response['status'] = 200
                response['message'] = 'Welcome'
            else:
                response['message'] = 'invalid password'
                raise Exception('invalid password')


        except Exception as e :
            print(e)

        return Response(response)




LoginView = LoginView.as_view()




class RegisterView(APIView):

    def post(self , request):
        response = {}
        response['status'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data

            if data.get('username') is None:
                response['message'] = 'key username not found'
                raise Exception('key username not found')

            if data.get('password') is None:
                response['message'] = 'key password not found'
                raise Exception('key password not found')


            check_user = User.objects.filter(username = data.get('username')).first()

            if check_user:
                response['message'] = 'username  already taken'
                raise Exception('username  already taken')

            user_obj = User.objects.create(email = data.get('username') , username = data.get('username'))
            user_obj.set_password(data.get('password'))
            user_obj.save()
            token = generate_random_string(10)
            Profile.objects.create(user = user_obj , token = token)
            #send_mail_to_user(token , data.get('username'))
            response['message'] = 'User created '
            response['status'] = 200



        except Exception as e :
            print(e)

        return Response(response)


RegisterView = RegisterView.as_view()
