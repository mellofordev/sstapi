from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import departments,Profile
# Create your models here.
program_genders=(('m','Male'),
                 ('f','Female'),
                 ('a','All'),
                 )
program_types=(('g','Group'),
                 ('s','Solo')
                 )
program_main_list=(('music','Music'),
                 ('instruments','Instruments'),
                 ('dance','Dance'),
                 ('theatre','Theatre Events'),
                 ('finearts','Fine Arts'),
                 )
class DepartmentPoints(models.Model):
    department = models.CharField(max_length=7,choices=departments,default='CS')
    group_event_score = models.IntegerField(default=0)
    solo_event_score = models.IntegerField(default=0)
    overall_score = models.IntegerField(default=1)
    
    def __str__(self) -> str:
        return self.department
class Program(models.Model):
    name = models.CharField(max_length=100)
    slot_time =models.DateTimeField(default=timezone.now)
    program_gender_type = models.CharField(max_length=7,choices=program_genders,default='m')
    program_type = models.CharField(max_length=5,choices=program_types,default='g')
    program_comes_under = models.CharField(max_length=80,choices=program_main_list,default='music')
    registered_users=models.ManyToManyField('accounts.Profile',related_name='registered_user',blank=True)
    winner_first = models.ManyToManyField('accounts.Profile',related_name='first',blank=True)
    winner_second = models.ManyToManyField('accounts.Profile',related_name='second',blank=True)
    winner_third = models.ManyToManyField('accounts.Profile',related_name='third',blank=True)
    max_member_limit=models.IntegerField(default=1)
    def __str__(self) -> str:
        return self.name 
    
    def update_score(self):
        first = self.winner_first.all()
        second = self.winner_second.all()
        third = self.winner_third.all()

        if first:
            for winner in first:
                department = winner.department
                points_table, created = DepartmentPoints.objects.get_or_create(department=department)
                if self.program_type == 's':
                    points_table.solo_event_score += 5
                elif self.program_type == 'g':
                    points_table.group_event_score += 10
                points_table.save()
        if second:
            for winner in second:
                department = winner.department
                points_table, created = DepartmentPoints.objects.get_or_create(department=department)
                if self.program_type == 's':
                    points_table.solo_event_score += 3
                elif self.program_type == 'g':
                    points_table.group_event_score += 6
                points_table.save()
        if third:
            for winner in third:
                department = winner.department
                points_table, created = DepartmentPoints.objects.get_or_create(department=department)
                if self.program_type == 's':
                    points_table.solo_event_score += 1
                elif self.program_type == 'g':
                    points_table.group_event_score += 3
                points_table.save()

class Team(models.Model):
    team_lead = models.OneToOneField(User,related_name='team_lead',on_delete=models.CASCADE)
    members=models.ManyToManyField('accounts.Profile',related_name='members',blank=True)
    program=models.ForeignKey(Program,related_name='program_team',on_delete=models.CASCADE)
    share_link=models.SlugField(default=0)
    def __str__(self) -> str:
        return str(self.team_lead.profile.name+self.program.name)