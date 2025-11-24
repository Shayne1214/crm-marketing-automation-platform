from rest_framework import serializers
from .models import User, Account, Lead, Email, MessageTemplate, SubjectTemplate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class LeadSerializer(serializers.ModelSerializer):
    Email = serializers.EmailField(required=False)
    email = serializers.EmailField(source='Email', required=False)

    class Meta:
        model = Lead
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        # Handle both 'Email' and 'email' field names
        if 'email' in data:
            data['Email'] = data.pop('email')
        if 'Email' in data:
            data['Email'] = data['Email'].lower().strip()
        if not data.get('Email'):
            raise serializers.ValidationError({'Email': 'Email is required'})
        return data


class EmailSerializer(serializers.ModelSerializer):
    account_details = AccountSerializer(source='account', read_only=True)

    class Meta:
        model = Email
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_email(self, value):
        return value.lower().strip()


class MessageTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplate
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class SubjectTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectTemplate
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

