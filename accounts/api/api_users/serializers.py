from rest_framework import serializers, response, status
from rest_framework.reverse import reverse as api_reverse

from django.contrib.auth import get_user_model
UserModel = get_user_model()
from entries.models import Entry
from entries.api.serializers import EntryListSerializer
# from accounts.models import Profile
from django_countries.serializers import CountryFieldMixin
from django_countries.serializer_fields import CountryField


class UserSerializer(CountryFieldMixin, serializers.ModelSerializer):
    appreciated_entries = serializers.SerializerMethodField()
    changed_perception = serializers.SerializerMethodField()
    entryset = serializers.SerializerMethodField(read_only=True)
    country = CountryField(country_dict=True)
    date_joined = serializers.SerializerMethodField(read_only=True)
    user_uri = serializers.HyperlinkedIdentityField(
        view_name='users:detail',
        lookup_field='username',
    )
    username = serializers.CharField(required=False)
    # country = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserModel
        fields = [
            'username',
            'user_uri',
            'email',
            'entryset',
            'country',
            'date_joined',
            'changed_perception',
            'appreciated_entries',
            'image',
        ]

        read_only_fields = ['date_joined', 'entryset']

    def get_entryset(self, obj):
        qs = obj.entry_set.all().order_by('-created')[:10]
        return [f'api/entries/{obj.id}/' for obj in qs]

    def get_date_joined(self, obj):
        return obj.date_joined.strftime("%m/%d/%Y, %H:%M:%S")

    def get_appreciated_entries(self, obj):
        qs = obj.appreciated_entries.all().order_by('-created')[:10]
        data = {
            'count': obj.appreciated_entries.count(),
            'list': [f'api/entries/{obj.id}/' for obj in qs]
        }
        return data

    def get_changed_perception(self, obj):
        qs = obj.changed_perception_entries.all().order_by('-created')[:10]
        data = {
            'count': obj.changed_perception_entries.count(),
            'list': [f'api/entries/{obj.id}/' for obj in qs]
        }
        return data

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        image = validated_data.get("image")
        code = validated_data.get('country', None)
        if code is not None:
            instance.country = code
            instance.save()
        return instance


    
        
