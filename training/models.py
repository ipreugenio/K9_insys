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
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, related_name="k9", blank=True, null=True)
    deployment_area = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="deployment_area", blank=True, null=True)

    def __str__(self):
        handler = User.objects.get(id=self.handler)
        k9 = K9.objects.get(id=self.k9)
        handler_name = handler.name
        k9_name = k9.name
        return str(handler_name + " : " + k9_name)