from django.db import models
from django.utils.translation import ugettext_lazy as _
from account.models import CustomUser
class Map(models.Model):
    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'map'
        verbose_name = _('Map')
        verbose_name_plural = _('Maps')

    name = models.CharField(max_length=255, verbose_name=_('Map Name'), null=False, blank=False)

class Cities(models.Model):
    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'map_cities'
        verbose_name = _('Citie')
        verbose_name_plural = _('Cities')

    name = models.CharField(max_length=255, verbose_name=_('Citie Name'), null=False, blank=False)

class LogisticsNetwork(models.Model):
    def __str__(self):
        return f'{self.origin_city} - {self.destination_city} - {self.distance}'

    class Meta:
        db_table = 'map_logistics_network'
        verbose_name = _('Logistic Network')
        verbose_name_plural = _('Logistics Network')

    origin_city = models.ForeignKey(Cities, verbose_name=_('Origin City'), related_name='origin_city', null=False, blank=False, on_delete=models.CASCADE)
    destination_city = models.ForeignKey(Cities, verbose_name=_('Destination City'), related_name='destination_city', null=False, blank=False, on_delete=models.CASCADE)
    distance = models.CharField(max_length=255, verbose_name=_('Distance between cities'), null=False, blank=False)
    map_network = models.ForeignKey(Map, verbose_name=_('Map'), null=False, blank=False, on_delete=models.CASCADE)

class HistoryLogisticNetwork(models.Model):
    def __str__(self):
        return f'{self.user} - {self.logistic_network}'

    class Meta:
        db_table = 'map_logs_logistics_network'
        verbose_name = _('Logs Logistic Network')
        verbose_name_plural = _('Logs Logistics Network')

    user = models.ForeignKey(CustomUser, verbose_name=_('User'), null=False, blank=False, on_delete=models.CASCADE)
    logistic_network = models.ForeignKey(LogisticsNetwork, verbose_name=_('Logistics Network'), null=False, blank=False, on_delete=models.CASCADE)