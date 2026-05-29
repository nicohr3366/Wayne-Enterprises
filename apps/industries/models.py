from django.db import models


class ElectricRecord(models.Model):
    record_id = models.CharField(max_length=30, unique=True)
    date = models.DateField(null=True, blank=True)
    station_id = models.CharField(max_length=30, blank=True)
    station_name = models.CharField(max_length=200, blank=True)
    gotham_district = models.CharField(max_length=100, blank=True)
    station_type = models.CharField(max_length=100, blank=True)
    energy_generated_mwh = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    energy_consumed_mwh = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    peak_demand_mw = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    avg_demand_mw = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    renewable_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    outage_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    fuel_type = models.CharField(max_length=100, blank=True)
    grid_frequency_hz = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    transmission_loss_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fiscal_year = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.record_id} - {self.station_name}'
