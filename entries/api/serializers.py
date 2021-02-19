from rest_framework import serializers
from entries.models import Entry
# from accounts.models import Profile
import datetime


class EntryDetailSerializer(serializers.ModelSerializer):
    user_uri = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='users:detail',
        lookup_field='username',
        source='user',
    )
    user_country = serializers.SerializerMethodField(read_only=True)
    user_country_name = serializers.SerializerMethodField(read_only=True)
    user = serializers.StringRelatedField()
    stats = serializers.SerializerMethodField(read_only=True)
    created = serializers.SerializerMethodField(read_only=True)
    updated = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Entry
        exclude= []
        read_only_fields = ['id', 'created', 'updated']
        extra_kwargs = {'content': {'required': False}, 'title': {'required': False}}
    

    def get_stats(self, obj):
        user = self.context.get("user")
        data = {
            'is_appreciated_by_user': user in obj.appreciated.all(),
            'changed_perc_of_user': user in obj.changed_perc.all(),
            'appreciated_count': obj.appreciated.count(),
            'changed_perceptions_count': obj.changed_perc.count(),
        }
        return data

    def get_user_country(self, obj):
        return obj.user.country.code

    def get_user_country_name(self, obj):
        return obj.user.country.name

    def get_created(self, obj):
        return obj.created.strftime("%m/%d/%Y")
    
    def get_updated(self, obj):
        return obj.updated.strftime("%m/%d/%Y")
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance

    def validate_title(self, value):
        if len(value) > 100:
            raise serializers.ValidationError('This title is too long')
        return value

    def validate_content(self, value):
        if len(value) > 1000:
            raise serializers.ValidationError('This content is too long')
        return value




class EntryListSerializer(serializers.ModelSerializer):
    user_uri = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='users:detail',
        lookup_field='username',
        source='user'
        )
    user = serializers.StringRelatedField()
    entry = serializers.HyperlinkedIdentityField(
        view_name='entries:detail',
        lookup_field='id',
        )
    user_country = serializers.SerializerMethodField(read_only=True)
    stats = serializers.SerializerMethodField(read_only=True)
    created = serializers.SerializerMethodField(read_only=True)
    updated = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Entry
        fields = '__all__'
        read_only_fields = ['user_uri', 'id', 'user', 'created', 'updated', 'user_country']

    def get_created(self, obj):
        return obj.updated.strftime("%m/%d/%Y")

    def get_updated(self, obj):
        return obj.updated.strftime("%m/%d/%Y")
    
    def get_user_country(self, obj):
        return obj.user.country.code

    def get_stats(self, obj):
        user = self.context.get("request").user
        print('entry serializer', user)
        data = {
            'is_appreciated_by_user': user in obj.appreciated.all(),
            'changed_perc_of_user': user in obj.changed_perc.all(),
            'appreciated_count': obj.appreciated.count(),
            'changed_perceptions_count': obj.changed_perc.count(),
        }
        return data
    ## one post per day validation
    def validate(self, data):
        user=self.context.get("request").user
        most_recent = Entry.objects.filter(user=user).order_by('-created').first()
        if isinstance(most_recent, Entry):
            if most_recent.created.date() == datetime.datetime.now().date():
                raise serializers.ValidationError('Sorry but you can only post one diary entry per day')
        return data

    def create(self, validated_data):
        user = self.context.get("request").user
        entry = Entry(user=user, **validated_data)
        entry.save()
        return entry


