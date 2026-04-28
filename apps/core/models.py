from django.db import models


class DefenseContract(models.Model):
    # Identifiers
    contract_id = models.CharField(max_length=100, unique=True)
    contract_number = models.CharField(max_length=100, blank=True)
    uei_number = models.CharField(max_length=50, blank=True)
    cage_code = models.CharField(max_length=20, blank=True)
    fpds_transaction_id = models.CharField(max_length=100, blank=True)

    # Parties
    agency = models.CharField(max_length=200)
    contractor_name = models.CharField(max_length=200, blank=True)

    # Financial
    obligated_amount_usd = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    contract_ceiling_usd = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    modification_amount_usd = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    # ETL / XML
    etl_source_system = models.CharField(max_length=100, blank=True)
    xml_schema_version = models.CharField(max_length=50, blank=True)
    data_feed_format = models.CharField(max_length=100, blank=True)

    # Classification
    security_classification = models.CharField(max_length=100, blank=True)
    naics_code = models.CharField(max_length=20, blank=True)
    naics_description = models.CharField(max_length=200, blank=True)
    psc_code = models.CharField(max_length=20, blank=True)
    cyber_compliance_level = models.CharField(max_length=100, blank=True)

    # Dates
    award_date = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    fiscal_year = models.IntegerField(null=True, blank=True)

    # Performance
    performance_status = models.CharField(max_length=100, blank=True)

    # Set-aside flags
    small_business = models.BooleanField(default=False)
    veteran_owned = models.BooleanField(default=False)
    women_owned = models.BooleanField(default=False)
    hubzone = models.BooleanField(default=False)

    # Location
    place_of_performance_state = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-obligated_amount_usd']
        verbose_name = 'Defense Contract'
        verbose_name_plural = 'Defense Contracts'

    def __str__(self):
        return f"{self.contract_number} — {self.agency}"
