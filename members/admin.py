from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Member, Document, SignedDocument


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'is_staff', 'is_active']
    search_fields = ['email', 'username']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'status', 'phone', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['first_name', 'last_name', 'phone', 'user__email']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_required', 'created_at']
    list_filter = ['is_required']


@admin.register(SignedDocument)
class SignedDocumentAdmin(admin.ModelAdmin):
    list_display = ['member', 'document', 'signed_at', 'ip_address']
    list_filter = ['signed_at']
    search_fields = ['member__first_name', 'member__last_name', 'document__title']
