from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect
# Create your views here.
@api_view(['POST'])
def signup_view(request):
    if request.method=='POST':
        response={}
        print("activated")
        #userData=Client.login(request.data['username'],request.data['username'])
        if request.data['isLoggedIn']=='True':
            user=User(
            username=request.data['username'],
            email='dummy@sctarts.com'
            )
            password =request.data['password']
            user.set_password(password)
            user.save()
            response['status']='User registered successfully'
            get_user=User.objects.get(username=request.data['username'])
            print(get_user)
            get_user.profile.name = request.data['name']
            if request.data['gender']=='Male':
                get_user.profile.gender='m'
            else:
                get_user.profile.gender='f'
            get_user.profile.department=request.data['department_id'][5:7]
            get_user.profile.year=4-int(request.data['department_id'][4:5])
            get_user.profile.chest_number=get_user.id
            get_user.save()
            token,obj=Token.objects.get_or_create(user=get_user)
            response['token']=str(token)
        else:
            return Response({"error":"Check your username or password !"})
        return Response(response)
def client_signup(request):
    return redirect('http://localhost:8501')