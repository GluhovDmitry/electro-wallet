from typing import List

from django.db import models
from django.db.models.query import QuerySet


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

    @staticmethod
    def get_users(filters: dict) -> QuerySet:
        """
        Get users by filters
        :param filters: filters
        :return: users
        """
        return WalletUser.objects.filter(deleted=False, **filters)

    @staticmethod
    def create_users(users: List[dict]) -> QuerySet:
        """
        Create users
        :param users: list of users. Example:
        [
            {
                'id': 1,
                'name': 'test_user'
            },
            {
                'id': 2,
                'name': 'test_user2'
            }
        ]
        :return: users
        """
        balance_objs = Balance.objects.bulk_create([Balance() for _ in users])
        users_objs = [WalletUser(**user, balance_id=balance_objs[idx].id) for idx, user in enumerate(users)]
        users = WalletUser.objects.bulk_create(users_objs)

        return users

    @staticmethod
    def update_users(users: dict) -> int:
        """
        Update users
        :param users: dict of users. Example:
        {
            1: {
                'name': 'Vasya'
            },
            2: {
                'name': 'Petya'
            },
        }
        :return: updated objs number
        """
        users_objs = WalletUser.objects.filter(id__in=users.keys())
        fields_on_update = ['name', ]
        for user in users_objs:
            for attr in fields_on_update:
                value = users[str(user.id)].get(attr)
                if value is not None:
                    setattr(user, attr, users[str(user.id)].get(attr))

        return WalletUser.objects.bulk_update(users_objs, fields_on_update)

    @staticmethod
    def delete_users(users_ids: list) -> int:
        """
        Mark users as deleted
        :param users_ids: dict of users. Example: [1, 2]
        :return: updated objs number
        """
        user_objs = WalletUser.objects.filter(
                deleted=False,
                id__in=users_ids)
        list(map(lambda tr: setattr(tr, 'deleted', True), user_objs))
        removed_users = WalletUser.objects.bulk_update(user_objs, ['deleted'])
        return removed_users

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

    @staticmethod
    def get_transactions(filters: dict) -> QuerySet:
        """
        Get transactions by filters
        :param filters: filters
        :return: transactions
        """
        return Transaction.objects.filter(deleted=False, **filters)

    @staticmethod
    def create_transactions(transactions: List[dict]) -> QuerySet:
        """
        Create transactions
        :param transactions: list of transactions. Example
        [
            {
                'user_id': 1,
                'date': '2023-07-05',
                'price_value': 500,
            },
            {
                'user_id': 2,
                'date': '2023-07-05',
                'price_value': 1000,
            }
        ]
        :return: transactions
        """
        transactions_objs = [Transaction(**transaction) for transaction in transactions]
        transactions_objs = Transaction.objects.bulk_create(transactions_objs)
        for transaction_obj in transactions_objs:
            transaction_obj.user.balance.balance_value += transaction_obj.price_value
            transaction_obj.user.balance.save()
        return transactions_objs

    @staticmethod
    def update_transactions(transactions: dict) -> int:
        """
        Update transactions
        :param transactions: dict of transactions. Example:
        {
            25: {
                'price_value': 300,
            },
            26: {
                'price_value': 800,
            },
        }
        :return: updated objs number
        """
        transactions_objs = Transaction.objects.filter(id__in=transactions.keys())
        for transaction_obj in transactions_objs:
            transaction_obj.user.balance.balance_value -= transaction_obj.price_value
            transaction_obj.user.balance.balance_value += transactions[str(transaction_obj.id)]['price_value']
            transaction_obj.user.balance.save()

        fields_on_update = ['price_value', ]
        for user in transactions_objs:
            for attr in fields_on_update:
                value = transactions[str(user.id)].get(attr)
                if value is not None:
                    setattr(user, attr, transactions[str(user.id)].get(attr))

        return Transaction.objects.bulk_update(transactions_objs, fields_on_update)

    @staticmethod
    def delete_transactions(transactions_ids: List[int]) -> int:
        """
        Mark transactions as deleted
        :param transactions_ids: list of transactions ids. Example: [25, 26]
        :return: updated objs number
        """
        transactions_objs = Transaction.objects.filter(id__in=transactions_ids)
        for transaction_obj in transactions_objs:
            transaction_obj.user.balance.balance_value -= transaction_obj.price_value
            transaction_obj.user.balance.save()
        list(map(lambda tr: setattr(tr, 'deleted', True), transactions_objs))
        removed_transactions = Transaction.objects.bulk_update(transactions_objs, ['deleted'])
        return removed_transactions

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
