
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

genders=(('m','Male'),('f','Female'))
departments=(('CS','CS'),
             ('CL','CL'),
             ('BT','BT'),
             ('EC','EC'),
             ('ME','Mech'),
             ('MA','Auto'),
             ('MP','MP'),
             )
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name= models.CharField(max_length=50,blank=False)
    chest_number=models.IntegerField(null=True)
    gender= models.CharField(max_length=3, choices=genders, default='f')
    department=models.CharField(max_length=5,choices=departments,default='cs')
    year=models.IntegerField(default=0)
    solo_event_registered_count = models.IntegerField(default=0)
    group_event_registered_count = models.IntegerField(default=0)
    registered_events = models.ManyToManyField('artsapi.Program')
    def __str__(self):
        return self.user.profile.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()