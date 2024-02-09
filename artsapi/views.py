from django.shortcuts import render
from rest_framework.decorators import api_view,authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .models import Program,DepartmentPoints,Team
from .serializers import ProgramSerializer,DepartmentSerializer,TeamSerializers
# Create your views here.

@api_view(['GET'])
def test_programs_api(request): #test view for reference 
    programs = Program.objects.get(id=1)
    print(programs.registered_users.all())
    print(programs.winners.all())
    print(programs.winners_position.all())
    return Response({"data":'programs'})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def programs_api(request,slug):
    if request.user.is_anonymous:
        return Response({'error':'Token not provided'})
    if slug=="all":
        get_programs = Program.objects.all()
    else:    
        get_programs = Program.objects.filter(program_comes_under=slug)
    program_bucket=[]
    for program in get_programs:
        serializer=ProgramSerializer(program,context={"request":request})
        program_bucket.append(serializer.data)
    return Response({"data":program_bucket})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def department_api(request):
    if request.user.is_anonymous:
        return Response({'error':'Token not provided'})
    get_departments = DepartmentPoints.objects.all()
    response=[]
    for program in get_departments:
        serializer=DepartmentSerializer(program)
        response.append(serializer.data)
    return Response({"data":response})
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def program_register_api(request,slug):
    if request.method=='GET':
        get_user=request.user
        if get_user.is_anonymous:
            return Response({'error':'Token not provided'})
        try:
            program = Program.objects.get(id=slug)
            if (get_user.profile.group_event_registered_count<=2 
                or
                get_user.profile.solo_event_registered_count<=4
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
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def create_team(request,slug):
    get_user=request.user
    if get_user.is_anonymous:
        return Response({"error":"Token not provided "})
    try:
        program = Program.objects.get(id=slug)
        if (get_user.profile not in program.registered_users.all() 
            and  get_user.profile.group_event_registered_count<=2
            ):
            try:
                Team.objects.create(team_lead=get_user,share_link=get_user.username,program=program)
                get_user.profile.registered_events.add(program.id)
                get_user.profile.group_event_registered_count+=1
                program.registered_users.add(get_user.profile.id)
                get_user.save()
                return Response({"data":'Created Team successfully'})
            except IntegrityError:
                return Response({"data":"You cant lead multiple teams."})
        else:
            return Response({"error":'Already registered or limit exceeded'})
    except ObjectDoesNotExist:
        return Response({"error":'Program doesnot exits'})
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def join_team(request,slug):
    get_user=request.user
    if get_user.is_anonymous:
        return Response({"error":"Token not provided "})
    try:
        team=Team.objects.get(share_link=slug)
        program = team.program
        print(program.registered_users.all())
        if (get_user.profile not in program.registered_users.all() 
            and  get_user.profile.group_event_registered_count<=2
            ):

            if(team.team_lead.profile.department==get_user.profile.department):
                if(len(team.members.all())+1<=program.max_member_limit):
                    team.members.add(get_user.profile.id)
                    get_user.profile.registered_events.add(program.id)
                    get_user.profile.group_event_registered_count+=1
                    program.registered_users.add(get_user.profile.id)
                    get_user.save()
                    return Response({"data":'Joined Team successfully'})
                else:
                    return Response({"data":'Team limit reached'})
            else:
                return Response({"data":'Different Branch'})
        else:
            return Response({"data":'Already registered or limit exceeded'})
    except ObjectDoesNotExist:
        return Response({"data":'Program doesnot exits'})
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_team_members_api(request,slug):
    if request.user.is_anonymous:
        return Response({"error":'Token not provided'})
    try:
        team=Team.objects.get(share_link=slug)
        serializers=TeamSerializers(team)
        return Response({"data":serializers.data})
    except ObjectDoesNotExist:
        return Response({"data":'Team does not exits'})

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
def delete_program_api(request,slug):
    get_user = request.user
    if get_user.is_anonymous:
        return Response({"error":'Token not provided'})
    try:
        program=Program.objects.get(id=slug)
        profile=get_user.profile
        
        print(profile,program.registered_users.all())
        if program.program_type=='s' and profile in program.registered_users.all():
            program.registered_users.remove(profile.id)
            profile.registered_events.remove(program.id)
            profile.solo_event_registered_count-=1
            profile.save()
            return Response({"data":'Deleted'})
        elif program.program_type=='g' :
            get_teams=Team.objects.filter(program=program)
            
            for team in get_teams:
                print(profile,team.team_lead.profile)
                if profile in team.members.all():
                    team.members.remove(profile.id)
                    profile.registered_events.remove(program.id)
                    profile.group_event_registered_count-=1
                    profile.save()
                    program.registered_users.remove(profile.id)
                    return Response({"data":'Deleted'})
                elif profile == team.team_lead.profile:
                    print("lead",profile)
                    get_members=team.members.all()
                    for member in get_members:
                        program.registered_users.remove(member.id)
                        member.registered_events.remove(program.id)
                        member.group_event_registered_count-=1
                        member.save()
                    team.delete()
                    profile.registered_events.remove(program.id)
                    profile.group_event_registered_count-=1
                    profile.save()
                    program.registered_users.remove(profile.id)
                    return Response({"data":'Deleted'})
            else:
                return Response({"data":'You didnt register for this event'})
            
        elif profile not in program.registered_users.all():
            return Response({"data":'You didnt register for this event'})
    except ObjectDoesNotExist:
        return Response({'data':'Program doesnot exits'})
                    
        