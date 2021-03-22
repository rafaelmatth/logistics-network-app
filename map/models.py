from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class LogisticsNetwork(models.Model):
    def __str__(self):
        return '{} - {} - {}'.format(self.origin_city, self.destination_city, self.distance)

    class Meta:
        db_table = 'Logistics Network'
        verbose_name = _('Logistic Network')
        verbose_name_plural = _('Logistics Network')

    origin_city = models.CharField(max_length=255, verbose_name=_('Origin City'), null=False, blank=False)
    destination_city = models.CharField(max_length=255, verbose_name=_('Destination City'), null=False, blank=False)
    distance = models.DecimalField(max_digits=None, decimal_places=None, verbose_name=_('Distance between cities'))

class Map(models.Model):
    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        db_table = 'map'
        verbose_name = _('Map')
        verbose_name_plural = _('Maps')

    name = models.CharField(max_length=255, verbose_name=_('Map Name'), null=False, blank=False)
    logistics_network = models.ForeignKey(CustomUser, verbose_name=_('Logistics Network'), null=True, blank=True, on_delete=models.CASCADE)
