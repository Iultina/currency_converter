import requests
from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import CurrencyConversionSerializer


class CurrencyListViewSet(viewsets.ViewSet):
    """
    Returns a list of available currencies along with their respective codes.

    Retrieves the list of currencies from an external API and returns it as a JSON object.
    """
    def list(self, request):
        api_url = (
            'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies.json'
        )
        response = requests.get(api_url)
        if response.status_code == 200:
            currencies = response.json()
            serialized_currencies = []
            for code, name in currencies.items():
                serialized_currencies.append({code, name})
            return Response(serialized_currencies, status=status.HTTP_200_OK)
        return Response(
            {'error': 'API Error'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )


class CurrencyConversionViewSet(viewsets.ViewSet):
    """
    Handles currency conversion based on query parameters.

    Takes 'from', 'to', and 'value' as query parameters
    to perform a currency conversion.
    Returns the result as a JSON object.
    """

    def list(self, request):
        from_currency = request.query_params.get('from')
        to_currency = request.query_params.get('to')
        query_params = {
            'from_currency': from_currency.lower() if from_currency else None,
            'to_currency': to_currency.lower() if to_currency else None,
            'value': request.query_params.get('value')
        }
        serializer = CurrencyConversionSerializer(data=query_params)
        if serializer.is_valid():
            from_currency = serializer.validated_data['from_currency']
            to_currency = serializer.validated_data['to_currency']
            value = serializer.validated_data['value']
            api_url = (
                f'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{from_currency}/{to_currency}.json'
            )
            response = requests.get(api_url)
            if response.status_code == 200:
                rates = response.json()
                if to_currency in rates:
                    conversion_rate = rates[to_currency]
                    result = conversion_rate * value
                    serializer.validated_data['result'] = result
                    return Response(
                        {"result": result},
                        status=status.HTTP_200_OK
                    )
            return Response(
                {'error': 'Invalid currency'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
