from rest_framework import serializers
from .models import Program,DepartmentPoints
from django.core.exceptions import ObjectDoesNotExist
class ProgramSerializer(serializers.ModelSerializer):
    registered_users=serializers.SerializerMethodField()
    winners=serializers.SerializerMethodField()
    is_registered=serializers.SerializerMethodField()
    class Meta:
        model=Program
        fields=['id',
                'name',
                'program_type',
                'program_comes_under',
                'slot_time',
                'registered_users',
                'winners',
                'is_registered'
                ]
    def profileJsonSerializer(self,program):
        profile_bucket=[]
        for profile in program.registered_users.all():
            profile_bucket.append(profile.name)
        return profile_bucket
    def get_registered_users(self,obj):

        program = Program.objects.get(name=obj)
        return self.profileJsonSerializer(program)
    def get_winners(self,obj):

        program = Program.objects.get(name=obj)
        return self.profileJsonSerializer(program)
    def get_is_registered(self,obj):
        program = Program.objects.get(name=obj)
        try:
            if program in self.context["request"].user.profile.registered_events.all():
                return True
            else:
                return False
        except AttributeError:
            return False
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=DepartmentPoints
        fields='__all__'
    
class ProgramRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Program
        fields=['id']
    def save(self,obj):
        try:
            user = self.instance
            program =obj
            if program.program_type=='s' and user.solo_event_registered_count<=3:
                program.registered_users=user
            elif program.program_type=='g' and user.solo_event_registered_count<=5:
                program.registered_users=user
            else:
                return "Limit Exceeded for registering"
            program.save()
            return "Registered for program"
        except ObjectDoesNotExist:
            return "Program doesnot exist"