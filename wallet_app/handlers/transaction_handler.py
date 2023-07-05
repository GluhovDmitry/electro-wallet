from typing import List

from django.db.models.query import QuerySet

from wallet_app import models


class TransactionsOperations:
    @staticmethod
    def get_transactions(filters: dict) -> QuerySet:
        """
        Get transactions by filters
        :param filters: filters
        :return: transactions
        """
        return models.Transaction.objects.filter(deleted=False, **filters)

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
        transactions_objs = [models.Transaction(**transaction) for transaction in transactions]
        transactions_objs = models.Transaction.objects.bulk_create(transactions_objs)
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
        transactions_objs = models.Transaction.objects.filter(id__in=transactions.keys())
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

        return models.Transaction.objects.bulk_update(transactions_objs, fields_on_update)

    @staticmethod
    def delete_transactions(transactions_ids: List[int]) -> int:
        """
        Mark transactions as deleted
        :param transactions_ids: list of transactions ids. Example: [25, 26]
        :return: updated objs number
        """
        transactions_objs = models.Transaction.objects.filter(id__in=transactions_ids)
        for transaction_obj in transactions_objs:
            transaction_obj.user.balance.balance_value -= transaction_obj.price_value
            transaction_obj.user.balance.save()
        list(map(lambda tr: setattr(tr, 'deleted', True), transactions_objs))
        removed_transactions = models.Transaction.objects.bulk_update(transactions_objs, ['deleted'])
        return removed_transactions