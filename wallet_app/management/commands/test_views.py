from loguru import logger

from django.test.client import Client
from django.core.management.base import BaseCommand


def test_get_user(client):
    body = {
        'filters': {
                'id': 1,
                'name': 'test_user'
            }
    }
    response = client.post(
        '/wallet/api/manage-user',
        body,
        content_type='application/json'
    )
    assert response.status_code == 200
    logger.info(response.json())


def test_create_user(client):
    body = {
        'users': [
            {
                'id': 1,
                'name': 'test_user'
            },
            {
                'id': 2,
                'name': 'test_user2'
            }
        ]
    }
    response = client.put(
        '/wallet/api/manage-user',
        body,
        content_type='application/json'
    )
    assert response.status_code == 200
    logger.info(response.json())


def test_update_user(client):
    body = {
        'users': {
            1: {
                'name': 'Vasya'
            },
            2: {
                'name': 'Petya'
            },
        }
    }
    response = client.patch(
        '/wallet/api/manage-user',
        body,
        content_type='application/json'
    )
    assert response.status_code == 200
    logger.info(response.json())


def test_delete_user(client):
    body = {
        'users_ids': [1, 2]
    }
    response = client.delete(
        '/wallet/api/manage-user',
        body,
        content_type='application/json'
    )
    assert response.status_code == 200
    logger.info(response.json())


def test_get_transaction(client):
    body = {
        'filters': {
                'date': '2023-07-05',
                'price_value': 1000
            }
    }
    response = client.post(
        '/wallet/api/manage-transactions',
        body,
        content_type='application/json'
    )
    assert response.status_code == 200
    logger.info(response.json())


def test_create_transaction(client):
    body = {
        'transactions': [
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
    }
    response = client.put(
        '/wallet/api/manage-transactions',
        body,
        content_type='application/json'
    )
    assert response.status_code == 200
    logger.info(response.json())


def test_update_transaction(client):
    body = {
        'transactions': {
            25: {
                'price_value': 300,
            },
            26: {
                'price_value': 800,
            },
        }
    }
    response = client.patch(
        '/wallet/api/manage-transactions',
        body,
        content_type='application/json'
    )
    assert response.status_code == 200
    logger.info(response.json())


def test_delete_transaction(client):
    body = {
        'transactions_ids': [25, 26]
    }
    response = client.delete(
        '/wallet/api/manage-transactions',
        body,
        content_type='application/json'
    )
    assert response.status_code == 200
    logger.info(response.json())


def test_ratings(client):
    response = client.get(
        '/wallet/api/ratings',
        content_type='application/json'
    )
    assert response.status_code == 200
    logger.info(response.json())


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = Client()

        # test_create_user(client)
        # test_get_user(client)
        # test_update_user(client)
        # test_delete_user(client)
        #
        # test_create_transaction(client)
        # test_get_transaction(client)
        # test_update_transaction(client)
        # test_delete_transaction(client)
        test_ratings(client)


