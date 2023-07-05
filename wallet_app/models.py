
from django.db import models


class WalletUser(models.Model):
    name = models.CharField(
        verbose_name='Имя',
        max_length=254,
        blank=True
    )
    balance = models.OneToOneField(
        'Balance',
        verbose_name='Баланс',
        on_delete=models.CASCADE,
        null=True
    )
    deleted = models.BooleanField(verbose_name='Удален', default=False)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'balance': self.balance.balance_value,
        }

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Transaction(models.Model):
    price_value = models.FloatField(verbose_name='Значение', default=0)
    date = models.DateTimeField(verbose_name='Дата', editable=False)
    deleted = models.BooleanField(verbose_name='Удален', default=False)
    user = models.ForeignKey(
        'WalletUser',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        null=True
    )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'price_value': self.price_value,
            'date': self.date,
            'user': self.user.name,
        }

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'


class Balance(models.Model):
    balance_value = models.FloatField(verbose_name='Значение', default=0)

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Баланс'
