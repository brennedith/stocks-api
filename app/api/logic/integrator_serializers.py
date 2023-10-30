from rest_framework import serializers

class IntegrationRequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)

class IntegrationRequestResponseObject(serializers.Serializer):
    actions: serializers.CharField()
    transaction_type: serializers.CharField()
    symbol: serializers.CharField()
    quantity: serializers.CharField()
    type: serializers.CharField()
    price_status: serializers.CharField()
    fee: serializers.CharField()
    date_time: serializers.CharField()

class IntegrationRequestResponse(serializers.ListSerializer):
    child = IntegrationRequestResponseObject()