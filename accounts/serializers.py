from rest_framework import serializers
from .models import Profile
from artsapi.models import Team
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    group_registered_events=serializers.SerializerMethodField()
    solo_registered_events=serializers.SerializerMethodField()
    
    class Meta:
        model =Profile
        fields=['id','username','name','department',
                'solo_event_registered_count',
                'group_event_registered_count',
                'chest_number','group_registered_events',
                'solo_registered_events'
                ]
    def get_username(self,obj):
        return obj.user.username
    def group_createdby(self, profile):
        for team in Team.objects.all():
            for profile_registered_events in profile.registered_events.all():
                if profile_registered_events == team.program:
                    if profile.user == team.team_lead.user:
                        return team.team_lead.user.username
                    elif profile in team.members.all():
                        return team.team_lead.user.username
        return None
    def get_group_registered_events(self,obj):
        registered_=[]
        for program in obj.registered_events.all():
            if program.program_type=='g':
                get_lead =self.group_createdby(obj)
                registered_.append({"program":{"name":program.name,"id":program.id,"created_by":get_lead.profile.name}})
        return registered_
    def get_solo_registered_events(self,obj):
        registered_=[]
        for program in obj.registered_events.all():
            if program.program_type=='s':
                registered_.append({"program":{"name":program.name,"id":program.id}})
        return registered_