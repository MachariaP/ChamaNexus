from django.contrib import admin
from django.utils.html import format_html
from .models import Member, Transaction, ChamaGroup


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'role', 'status', 'net_balance_display', 'created_at']
    list_filter = ['role', 'status', 'created_at']
    search_fields = ['name', 'phone_number']
    readonly_fields = ['id', 'created_at', 'updated_at', 'net_balance_display']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'phone_number', 'user')
        }),
        ('Chama Details', {
            'fields': ('role', 'status')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at', 'net_balance_display'),
            'classes': ('collapse',)
        }),
    )
    
    def net_balance_display(self, obj):
        """Display member's net balance"""
        balance = obj.calculate_net_balance()
        color = 'green' if balance >= 0 else 'red'
        return format_html(
            '<span style="color: {};">KES {:,.2f}</span>',
            color,
            balance
        )
    net_balance_display.short_description = 'Net Balance'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['mpesa_code', 'member', 'transaction_type', 'amount', 'status', 'date', 'created_by']
    list_filter = ['transaction_type', 'status', 'date', 'created_at']
    search_fields = ['mpesa_code', 'member__name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at', 'verified_at', 'verified_by']
    autocomplete_fields = ['member']
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('member', 'transaction_type', 'amount', 'mpesa_code', 'date', 'description')
        }),
        ('Status', {
            'fields': ('status', 'verified_at', 'verified_by')
        }),
        ('Audit Information', {
            'fields': ('id', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Automatically set created_by to current user if not set"""
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    actions = ['verify_transactions', 'reject_transactions']
    
    def verify_transactions(self, request, queryset):
        """Bulk verify transactions"""
        count = 0
        for transaction in queryset:
            if transaction.status == 'PENDING':
                transaction.verify(request.user)
                count += 1
        self.message_user(request, f'{count} transaction(s) verified.')
    verify_transactions.short_description = 'Verify selected transactions'
    
    def reject_transactions(self, request, queryset):
        """Bulk reject transactions"""
        count = 0
        for transaction in queryset:
            if transaction.status == 'PENDING':
                transaction.reject(request.user)
                count += 1
        self.message_user(request, f'{count} transaction(s) rejected.')
    reject_transactions.short_description = 'Reject selected transactions'


@admin.register(ChamaGroup)
class ChamaGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'monthly_contribution_amount', 'total_balance_display', 'created_at']
    readonly_fields = ['id', 'created_at', 'updated_at', 'total_balance_display', 'total_fines_display']
    
    fieldsets = (
        ('Group Information', {
            'fields': ('name', 'description', 'monthly_contribution_amount')
        }),
        ('Financial Summary', {
            'fields': ('total_balance_display', 'total_fines_display')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def total_balance_display(self, obj):
        """Display group's total balance"""
        balance = obj.calculate_total_balance()
        return format_html(
            '<span style="color: green; font-weight: bold;">KES {:,.2f}</span>',
            balance
        )
    total_balance_display.short_description = 'Total Group Balance'
    
    def total_fines_display(self, obj):
        """Display total fines collected"""
        fines = obj.get_total_fines()
        return format_html(
            '<span style="color: orange;">KES {:,.2f}</span>',
            fines
        )
    total_fines_display.short_description = 'Total Fines Collected'
