from django.db import models

class TransactionHistory(models.Model):
  actions = models.CharField(max_length=24)
  transaction_type = models.CharField(max_length=64)
  symbol = models.CharField(max_length=24)
  quantity = models.CharField(max_length=64)
  type = models.CharField(max_length=64)
  price_status = models.CharField(max_length=64)
  fee = models.CharField(max_length=64)
  date_time = models.CharField(max_length=64)
  source = models.CharField(max_length=64)
  date_added = models.DateField(auto_now_add=True)
