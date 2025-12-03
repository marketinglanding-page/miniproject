from django.db import models
from accounts.models import Account


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('DEPOSIT', '입금'),
        ('WITHDRAW', '출금'),
    ]

    TRANSACTION_METHOD_CHOICES = [
        ('BANK_TRANSFER', '은행 이체'),
        ('CARD', '카드 결제'),
        ('CASH', '현금'),
        ('ETC', '기타'),
    ]

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name="계좌"
    )

    transaction_type = models.CharField(
        verbose_name="입금/출금",
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES
    )

    transaction_method = models.CharField(
        verbose_name="거래방식",
        max_length=20,
        choices=TRANSACTION_METHOD_CHOICES
    )

    amount = models.BigIntegerField(verbose_name="금액(원 단위)")

    balance_after = models.BigIntegerField(verbose_name="거래 후 잔액")

    transaction_details = models.CharField(verbose_name="상세내역", max_length=255)

    transaction_timestamp = models.DateTimeField(verbose_name="거래일시")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    class Meta:
        db_table = 'transactions'
        verbose_name = '거래 내역'
        ordering = ['-transaction_timestamp'] 

    def __str__(self):
        return f"[{self.transaction_timestamp.date()}] {self.account.account_number} | {self.transaction_type}: {self.amount}"
