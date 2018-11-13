from django.db import models
from planningandacquiring.models import K9
from profiles.models import User
from deployment.models import Team

# Create your models here.


class K9_Genealogy(models.Model):
    o = models.ForeignKey(K9, on_delete=models.CASCADE, blank=True, null=True)
    m = models.ForeignKey(K9, on_delete=models.CASCADE, related_name="m", blank=True, null=True)
    f = models.ForeignKey(K9, on_delete=models.CASCADE, related_name="f", blank=True, null=True)
    depth = models.IntegerField('depth',default=0) # family tree level
    zero = models.ForeignKey(K9, on_delete=models.CASCADE, related_name="zero", blank=True, null=True) #latest born

class K9_Handler(models.Model):
    handler = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "handler", blank=True, null=True)
<<<<<<< HEAD
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, related_name="k9", blank=True, null=True)
    deployment_area = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="deployment_area", blank=True, null=True)

    def __str__(self):
        handler = User.objects.get(id=self.handler)
        k9 = K9.objects.get(id=self.k9)
        handler_name = handler.name
        k9_name = k9.name
        return str(handler_name + " : " + k9_name)
=======
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, blank=True, null=True)

class Training(models.Model):
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, blank=True, null=True)
    stage = models.CharField('stage', max_length=200, default="Stage 0")
    stage1_1 = models.BooleanField(default=False)
    stage1_2 = models.BooleanField(default=False)
    stage1_3 = models.BooleanField(default=False)
    stage2_1 = models.BooleanField(default=False)
    stage2_2 = models.BooleanField(default=False)
    stage2_3 = models.BooleanField(default=False)
    stage3_1 = models.BooleanField(default=False)
    stage3_2 = models.BooleanField(default=False)
    stage3_3 = models.BooleanField(default=False)
    grade = models.CharField('grade', max_length=50, default='No Grade Yet')
    remarks = models.CharField('remarks', max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.k9) +' - ' + str(self.stage)
>>>>>>> 5c7ee24edce3e0a440abb53c2307dc112f109dae
