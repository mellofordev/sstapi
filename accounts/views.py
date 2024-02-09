from rest_framework.decorators import api_view,authentication_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Profile
from .serializers import ProfileSerializer
# Create your views here.
@api_view(['POST'])
def signup_view(request):
    if request.method=='POST':
        response={}
        print("activated")
        #userData=Client.login(request.data['username'],request.data['username'])
        if request.data['isLoggedIn']=='True':
            try:
                get_user_ = User.objects.get(username=request.data['username'])
                print(get_user_)
                token,obj=Token.objects.get_or_create(user=get_user_)
                return Response({"token":token.key})
            except ObjectDoesNotExist:   
                user=User(
                username=request.data['username'],
                email='dummy@sctarts.com'
                )
                password =request.data['password']
                user.set_password(password)
                user.save()
                get_user=User.objects.get(username=request.data['username'])
                print(get_user)
                get_user.profile.name = request.data['name']
                if request.data['gender']=='Male':
                    get_user.profile.gender='m'
                else:
                    get_user.profile.gender='f'
                get_user_department=request.data['department_id']
                if(len(get_user_department)==10):
                    get_user_department=request.data['department_id'][5:7]
                    if( get_user_department=="ME" or get_user_department=="EC" ):
                        get_user.profile.department='default'
                    else:
                        get_user.profile.department=request.data['department_id'][5:7]
                    get_user.profile.year=4-int(request.data['department_id'][4:5])
                elif(len(get_user_department)==11):
                    get_user_department=request.data['department_id'][6:8]
                    if( get_user_department=="ME" or get_user_department=="EC" ):
                        get_user.profile.department='default'
                    else:
                        get_user.profile.department=request.data['department_id'][5:7]
                    get_user.profile.year=4-int(request.data['department_id'][5:6])
                get_user.profile.chest_number=get_user.id
                get_user.save()
                token,obj=Token.objects.get_or_create(user=get_user)
                response['token']=str(token)
                
        else:
            return Response({"error":"Check your username or password !"})
        return Response(response)
def client_signup(request):
    return redirect('http://localhost:8501')

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def profile_api(request):
    get_user=request.user
    if get_user.is_anonymous:
        return Response({"error":'Token not provided '})
    try:
        profile = Profile.objects.get(user=get_user)
        serializer= ProfileSerializer(profile)
    except ObjectDoesNotExist:
        return Response({"error":"Token not provided"})
    return Response({"data":serializer.data})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def profile_department_set_api(request,slug):
    get_user=request.user 
    if get_user.is_anonymous:
        return Response({'error':'Token not provided'})
    try:
        profile = get_user.profile
        if profile.department=='default':
            profile.department=slug
            print(slug)
            profile.save()
            return Response({'data':'updated'})
        else:
            return Response({'data':"Cannot set department for this user"})
    except ObjectDoesNotExist:
        return Response({'error':'User doest not exists'})
    