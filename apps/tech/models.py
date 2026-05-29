from django.db import models


class TumblerTelemetry(models.Model):
    record_id = models.CharField(max_length=30, unique=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    vehicle_id = models.CharField(max_length=30, blank=True)
    vehicle_model = models.CharField(max_length=100, blank=True)
    mission_id = models.CharField(max_length=30, blank=True)
    mission_type = models.CharField(max_length=100, blank=True)
    speed_kmh = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    fuel_level_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    engine_temp_c = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    battery_level_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    gotham_zone = models.CharField(max_length=100, blank=True)
    alert_type = models.CharField(max_length=100, blank=True)
    system_status = models.CharField(max_length=50, default='operational')
    distance_km = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.record_id} - {self.vehicle_model}'
