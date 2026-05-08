from django.db import models

class CyberSecurityRecord(models.Model):
    incident_id = models.CharField(max_length=100)
    threat_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=50)
    affected_system = models.CharField(max_length=200)
    detected_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=100)

    class Meta:
        ordering = ['-detected_at']

    def __str__(self):
        return f"{self.threat_type} - {self.severity}"