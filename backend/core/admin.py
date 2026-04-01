from django.contrib import admin
from .models import Expense, ExpenseCategory, ExpenseReport

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "amount", "date", "submitted_by", "created_at"]
    list_filter = ["category", "status"]
    search_fields = ["title", "submitted_by"]

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "budget", "spent", "period", "manager", "created_at"]
    list_filter = ["period"]
    search_fields = ["name", "manager"]

@admin.register(ExpenseReport)
class ExpenseReportAdmin(admin.ModelAdmin):
    list_display = ["title", "submitted_by", "total", "items_count", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["title", "submitted_by", "period"]
