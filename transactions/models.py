from django.db import models
from accounts.models import Account # Account 모델 임포트

class Transaction(models.Model):
    account = models.ForeignKey(
        Account, # accounts.Account 참조
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name="계좌"
    )
    transaction_type = models.CharField(verbose_name="입금/출금", max_length=10)
    transaction_method = models.CharField(verbose_name="거래방식", max_length=20)
    amount = models.BigIntegerField(verbose_name="금액(원 단위)")
    balance_after = models.BigIntegerField(verbose_name="거래후잔액(원 단위)")
    transaction_details = models.CharField(verbose_name="상세내역", max_length=255)
    transaction_timestamp = models.DateTimeField(verbose_name="거래일시")

    class Meta:
        db_table = 'transactions'
        verbose_name = '거래 내역'
        ordering = ['-transaction_timestamp']

