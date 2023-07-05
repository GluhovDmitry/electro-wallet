from typing import List

from django.db.models.query import QuerySet

from wallet_app import models


class UsersOperations:
    @staticmethod
    def get_users(filters: dict) -> QuerySet:
        """
        Get users by filters
        :param filters: filters
        :return: users
        """
        return models.WalletUser.objects.filter(deleted=False, **filters)

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
        balance_objs = models.Balance.objects.bulk_create([models.Balance() for _ in users])
        users_objs = [models.WalletUser(**user, balance_id=balance_objs[idx].id) for idx, user in enumerate(users)]
        users = models.WalletUser.objects.bulk_create(users_objs)

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
        users_objs = models.WalletUser.objects.filter(id__in=users.keys())
        fields_on_update = ['name', ]
        for user in users_objs:
            for attr in fields_on_update:
                value = users[str(user.id)].get(attr)
                if value is not None:
                    setattr(user, attr, users[str(user.id)].get(attr))

        return models.WalletUser.objects.bulk_update(users_objs, fields_on_update)

    @staticmethod
    def delete_users(users_ids: list) -> int:
        """
        Mark users as deleted
        :param users_ids: dict of users. Example: [1, 2]
        :return: updated objs number
        """
        user_objs = models.WalletUser.objects.filter(
            deleted=False,
            id__in=users_ids)
        list(map(lambda tr: setattr(tr, 'deleted', True), user_objs))
        removed_users = models.WalletUser.objects.bulk_update(user_objs, ['deleted'])
        return removed_users

