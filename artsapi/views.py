from django.shortcuts import render
from rest_framework.decorators import api_view,authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ObjectDoesNotExist
from .models import Program,DepartmentPoints
from .serializers import ProgramSerializer,DepartmentSerializer,ProgramRegisterSerializer
# Create your views here.

@api_view(['GET'])
def test_programs_api(request): #test view for reference 
    programs = Program.objects.get(id=1)
    print(programs.registered_users.all())
    print(programs.winners.all())
    print(programs.winners_position.all())
    return Response({"data":'programs'})

@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
def programs_api(request):
    #if request.user.is_anonymous:
    #    return Response({'error':'Token not provided'})
    get_programs = Program.objects.all()
    program_bucket=[]
    for program in get_programs:
        serializer=ProgramSerializer(program)
        program_bucket.append(serializer.data)
    return Response({"data":program_bucket})


@api_view(['GET'])
#@authentication_classes([TokenAuthentication])
def department_api(request):
    #if request.user.is_anonymous:
    #    return Response({'error':'Token not provided'})
    get_departments = DepartmentPoints.objects.all()
    response=[]
    for program in get_departments:
        serializer=DepartmentSerializer(program)
        response.append(serializer.data)
    return Response({"data":response})
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def program_register_api(request,slug):
    if request.method=='POST':
        get_user=request.user
        if get_user.is_anonymous:
            return Response({'error':'Token not provided'})
        try:
            program = Program.objects.get(id=slug)
            if (get_user.profile.solo_event_registered_count<=3 
                or
                get_user.profile.solo_event_registered_count<=5
                ):
                
                if get_user.profile not in program.registered_users.all():
                    program.registered_users.add(get_user.profile.id)
                    get_user.profile.registered_events.add(program.id)
                    if program.program_type=='s':
                        get_user.profile.solo_event_registered_count+=1
                    else:
                        get_user.profile.group_event_registered_count+=1
                    get_user.save()
                    return Response({"data":"Registered for the program"}) 
                else:
                    return Response({"error":"Already registered for the event !"}) 
            else:
                return Response({"error":'Limit exceeded for registering'})
        except ObjectDoesNotExist:
            return Response({"error":'Program does not exits'})