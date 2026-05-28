from django.db import models


class Property(models.Model):
    PROPERTY_TYPES = [
        ('residential', 'Residencial'),
        ('commercial', 'Comercial'),
        ('industrial', 'Industrial'),
        ('mixed', 'Uso Mixto'),
    ]

    name = models.CharField(max_length=200)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    location = models.CharField(max_length=200)
    description = models.TextField()
    area_sqft = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.location}"

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']

class UrbanProject(models.Model):

    project_id = models.CharField(max_length=20, unique=True)
    project_name = models.CharField(max_length=255)

    district = models.CharField(max_length=100)
    project_type = models.CharField(max_length=100)

    status = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)

    total_budget_musd = models.FloatField()
    executed_cost_musd = models.FloatField()

    physical_progress_pct = models.IntegerField()
    financial_progress_pct = models.IntegerField()

    security_incidents = models.IntegerField()

    contractor = models.CharField(max_length=255)

    def __str__(self):
        return self.project_name