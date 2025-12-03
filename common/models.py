from django.db import models

# Create your models here.
# common/models.py

class CommonCode(models.Model):
    category = models.CharField(verbose_name="코드분류", max_length=50)
    code = models.CharField(verbose_name="코드", max_length=50)
    description = models.CharField(verbose_name="설명", max_length=100)

    class Meta:
        db_table = 'common_codes'
        verbose_name = '공통 코드'
        unique_together = ('category', 'code')

    def __str__(self):
        return f'[{self.category}] {self.code}'