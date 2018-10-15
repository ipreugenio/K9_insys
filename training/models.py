from django.db import models
from planningandacquiring.models import K9

# Create your models here.


class K9_Genealogy(models.Model):
    o = models.ForeignKey(K9, on_delete=models.CASCADE, blank=True, null=True)
    m = models.ForeignKey(K9, on_delete=models.CASCADE, related_name="m", blank=True, null=True)
    f = models.ForeignKey(K9, on_delete=models.CASCADE, related_name="f", blank=True, null=True)
    depth = models.IntegerField('depth',default=0) # family tree level
    zero = models.ForeignKey(K9, on_delete=models.CASCADE, related_name="zero", blank=True, null=True) #latest born
