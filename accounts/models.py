
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

genders=(('m','Male'),('f','Female'))
departments=(('CS','CS'),
             ('AM','CL'),
             ('BT','BT'),
             ('ECA','ECA'),
             ('ECB','ECB'),
             ('MEA','Mech A'),
             ('MEB','Mech B'),
             ('MA','Auto'),
             ('MP','MP'),
             ('default','default')
             )
# class_choice=(
#              ('R2A','R2A'),('R4A','R2A'),('R6A','R6A'),('R8A','R8A'),
#              ('R2B','R2B'),('R4B','R4B'),('R4B','R4B'),('R4B','R4B'),
#              ('B2','B2'),('B4','B4'),('B6','B6'),('B8','B8')
#              ('T2A','T2A'),('T4A','T4A'),('T6A','T6A'),('T8A','T8A'),
#              ('T2B','T2B'),('T4B','T4B'),('T6B','T6B'),('T8B','T8B'),
#              ('M2A','M2A'),('M4A','M4A'),('M6A','M6A'),('M8A','M8A'),
#              ('M2B','M2B'),('M4B','M4B'),('M6B','M6B'),('M8B','M8B'),
#              ('A2','A2'),('A4','A4'),('A6','A6'),('A8','A8'),
#              ('P8','P8'),
#              ('default','default')
#              )
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name= models.CharField(max_length=50,blank=False)
    chest_number=models.IntegerField(null=True)
    gender= models.CharField(max_length=3, choices=genders, default='f')
    department=models.CharField(max_length=7,choices=departments,default='default')
    year=models.IntegerField(default=0)
    solo_event_registered_count = models.IntegerField(default=0)
    group_event_registered_count = models.IntegerField(default=0)
    registered_events = models.ManyToManyField('artsapi.Program',blank=True)
    def __str__(self):
        return self.user.profile.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()