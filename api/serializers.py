from rest_framework import serializers


class CurrencyConversionSerializer(serializers.Serializer):
    """
    Serializer for currency conversion.

    Fields:
        from_currency: The currency to convert from.
        to_currency: The currency to convert to.
        value: The amount to be converted.
        result: The converted value (read-only).
    """

    from_currency = serializers.CharField()
    to_currency = serializers.CharField()
    value = serializers.FloatField()
    result = serializers.FloatField(read_only=True)
