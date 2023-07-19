from django.contrib import admin

from .models import UserInquiry, EmailTemplate, EmailHistory


@admin.register(UserInquiry)
class UserInquiryAdmin(admin.ModelAdmin):
    list_display = ('email', 'received_date')
    search_fields = ('email', 'message')
    ordering = ('-received_date',)


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('template_name', 'email_subject', 'created_date', 'updated_date')
    search_fields = ('template_name', 'email_subject')
    ordering = ('-updated_date',)


@admin.register(EmailHistory)
class EmailHistoryAdmin(admin.ModelAdmin):
    list_display = ('template_name', 'email_subject', 'sent_to', 'sent_status', 'sent_date')
    search_fields = ('template_name', 'email_subject', 'sent_to', 'sent_status')
    ordering = ('-sent_date',)
