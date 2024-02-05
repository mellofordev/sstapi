from rest_framework import serializers
from .models import Profile
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
    def get_group_registered_events(self,obj):
        registered_=[]
        for program in obj.registered_events.all():
            if program.program_type=='g':
                registered_.append(program.name)
        return registered_
    def get_solo_registered_events(self,obj):
        registered_=[]
        for program in obj.registered_events.all():
            if program.program_type=='s':
                registered_.append(program.name)
        return registered_