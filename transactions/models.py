from django.db import models

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('INCOME', '수입'),
        ('EXPENSE', '지출'),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
    )
    description = models.CharField(max_length=255)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"[{self.date}] {self.transaction_type}: {self.amount}"