from rest_framework import serializers
from .models import Profile
class ProfileSerializer(serializers.ModelSerializer):
    registered_events=serializers.SerializerMethodField()
    class Meta:
        model =Profile
        fields=['username','name','deparment','solo_event_registered_count','group_event_registered_count','chest_number','solo','registered_events']

    def get_registered_events(self,obj):
        registered_=[]
        for program in obj:
            registered_.append(program.name)
        return registered_
