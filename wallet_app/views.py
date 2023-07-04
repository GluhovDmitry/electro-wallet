import json

from django.views import View
from django.http import JsonResponse, HttpRequest, HttpResponse

from . import models
from .handlers import ratings_handler


class UsersManager(View):
    """Users CRUD view"""
    def post(self, request: HttpRequest) -> JsonResponse:
        request_data = json.loads(request.body.decode('utf-8'))
        data = models.WalletUser.get_users(filters=request_data.get('filters', {}))
        return JsonResponse({'users': [item.to_dict() for item in data]})

    def put(self, request: HttpRequest) -> JsonResponse:
        request_data = json.loads(request.body.decode('utf-8'))
        users = request_data['users']
        data = models.WalletUser.create_users(users)
        return JsonResponse({'users': [item.to_dict() for item in data]})

    def delete(self, request: HttpRequest) -> JsonResponse:
        request_data = json.loads(request.body.decode('utf-8'))
        users_ids = request_data['users_ids']
        count = models.WalletUser.delete_users(users_ids)
        return JsonResponse({'count': count})

    def patch(self, request: HttpRequest) -> JsonResponse:
        request_data = json.loads(request.body.decode('utf-8'))
        users = request_data['users']
        count = models.WalletUser.update_users(users)
        return JsonResponse({'count': count})


class TransactionsManager(View):
    """Transactions CRUD view"""
    def post(self, request: HttpRequest) -> JsonResponse:
        request_data = json.loads(request.body.decode('utf-8'))
        data = models.Transaction.get_transactions(filters=request_data.get('filters', {}))
        return JsonResponse({'transactions': [item.to_dict() for item in data]})

    def put(self, request: HttpRequest) -> JsonResponse:
        request_data = json.loads(request.body.decode('utf-8'))
        transactions = request_data['transactions']
        data = models.Transaction.create_transactions(transactions)
        return JsonResponse({'transactions': [item.to_dict() for item in data]})

    def delete(self, request: HttpRequest) -> JsonResponse:
        request_data = json.loads(request.body.decode('utf-8'))
        transactions_ids = request_data['transactions_ids']
        count = models.Transaction.delete_transactions(transactions_ids)
        return JsonResponse({'count': count})

    def patch(self, request: HttpRequest) -> JsonResponse:
        request_data = json.loads(request.body.decode('utf-8'))
        transactions = request_data['transactions']
        count = models.Transaction.update_transactions(transactions)
        return JsonResponse({'count': count})


def get_ratings(request: HttpRequest) -> JsonResponse:
    """
    View top users data by transaction for the last six months
    :param request: request
    :return: rating. Example:
    {'rating':
        [{'name': 'Petya', 'price_value': 800.0, 'date': '2023-07-05T00:00:00Z'},
        {'name': 'Vasya', 'price_value': 300.0, 'date': '2023-07-05T00:00:00Z'}]
    }
    """
    if request.method == "GET":
        response = ratings_handler.transaction_rating()
        return JsonResponse({'rating': response})

