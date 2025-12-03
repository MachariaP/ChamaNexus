"""
Dashboard serializers for ChamaNexus API.
"""

from rest_framework import serializers


class MemberDashboardSerializer(serializers.Serializer):
    """Serializer for member dashboard data"""
    personal_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    group_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    next_meeting = serializers.DictField(required=False, allow_null=True)
    loan_status = serializers.DictField(required=False, allow_null=True)
    recent_transactions = serializers.ListField(required=False)
    contribution_summary = serializers.DictField(required=False)


class TreasurerDashboardSerializer(serializers.Serializer):
    """Serializer for treasurer dashboard data"""
    group_summary = serializers.DictField()
    recent_activity = serializers.ListField(required=False)
    pending_approvals = serializers.ListField(required=False)
    defaulters = serializers.ListField(required=False)


class DashboardSummarySerializer(serializers.Serializer):
    """Generic dashboard summary serializer"""
    user_role = serializers.CharField()
    data = serializers.DictField()
