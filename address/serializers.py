from rest_framework import serializers

from user_accounts.serializers import KanvasUserSerializer


class AddressSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    street = serializers.CharField()
    house_number = serializers.IntegerField()
    city = serializers.CharField()
    state = serializers.CharField()
    zip_code = serializers.CharField()
    country = serializers.CharField()
    users = KanvasUserSerializer(read_only=True, many=True)
