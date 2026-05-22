from django.db import models


class Property(models.Model):
    PROPERTY_TYPES = [
        ('residential', 'Residencial'),
        ('commercial', 'Comercial'),
        ('industrial', 'Industrial'),
        ('mixed', 'Uso Mixto'),
    ]

    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('under_construction', 'En Construcción'),
        ('planned', 'Planificado'),
        ('completed', 'Completado'),
    ]

    # Campos originales
    name = models.CharField(max_length=200)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    area_sqft = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Campos nuevos — dataset Desarrollo Urbano Gotham
    project_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    developer = models.CharField(max_length=200, blank=True)
    district = models.CharField(max_length=100, blank=True)
    floors = models.IntegerField(null=True, blank=True)
    year_built = models.IntegerField(null=True, blank=True)
    price_usd = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    market_value_usd = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    occupancy_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    project_status = models.CharField(max_length=30, choices=STATUS_CHOICES, blank=True)
    green_certified = models.BooleanField(default=False)
    smart_building = models.BooleanField(default=False)
    zoning_code = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} — {self.district}"

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        ordering = ['-market_value_usd']
