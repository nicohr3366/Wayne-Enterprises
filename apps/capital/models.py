from django.db import models


class StockRecord(models.Model):
    ticker = models.CharField(max_length=20)
    company_name = models.CharField(max_length=200)
    division = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    open_price = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    high_price = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    low_price = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    close_price = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    adj_close = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    volume = models.BigIntegerField(default=0)
    market_cap_usd = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dividend_yield = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    sector = models.CharField(max_length=100, blank=True)
    exchange = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-date', 'ticker']

    def __str__(self):
        return f'{self.ticker} - {self.date}'
