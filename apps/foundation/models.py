from django.db import models


class Donacion(models.Model):
    donation_id = models.CharField(max_length=30, unique=True)
    donor_name = models.CharField(max_length=200)
    donor_type = models.CharField(max_length=50)
    amount_usd = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    donation_date = models.DateField(null=True, blank=True)
    project_name = models.CharField(max_length=200, blank=True)
    project_category = models.CharField(max_length=100, blank=True)
    gotham_district = models.CharField(max_length=100, blank=True)
    purpose = models.CharField(max_length=500, blank=True)
    fiscal_year = models.IntegerField(null=True, blank=True)
    tax_deductible = models.BooleanField(default=True)
    matched = models.BooleanField(default=False)
    recurring = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default='completed')

    class Meta:
        ordering = ['-donation_date']

    def __str__(self):
        return f'{self.donation_id} - {self.donor_name}'
