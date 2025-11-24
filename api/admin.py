from django.contrib import admin
from .models import User, Account, Lead, Email, MessageTemplate, SubjectTemplate


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at', 'updated_at']
    search_fields = ['email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'first_name', 'last_name', 'main_email', 'created_at']
    search_fields = ['name', 'main_email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['Email', 'status', 'first_name', 'last_name', 'company', 'assigned_to', 'created_at']
    list_filter = ['status', 'assigned_to', 'created_at']
    search_fields = ['Email', 'first_name', 'last_name', 'company']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'account', 'created_at']
    search_fields = ['email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'industry', 'used', 'replied', 'succeeded', 'created_at']
    list_filter = ['industry', 'created_at']
    search_fields = ['content', 'industry']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SubjectTemplate)
class SubjectTemplateAdmin(admin.ModelAdmin):
    list_display = ['content', 'used', 'replied', 'succeeded', 'created_at']
    search_fields = ['content']
    readonly_fields = ['created_at', 'updated_at']

