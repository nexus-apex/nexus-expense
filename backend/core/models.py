from django.db import models

class Expense(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=[("travel", "Travel"), ("food", "Food"), ("office", "Office"), ("software", "Software"), ("equipment", "Equipment"), ("marketing", "Marketing")], default="travel")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateField(null=True, blank=True)
    submitted_by = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=50, choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected"), ("reimbursed", "Reimbursed")], default="pending")
    receipt_url = models.URLField(blank=True, default="")
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    period = models.CharField(max_length=50, choices=[("monthly", "Monthly"), ("quarterly", "Quarterly"), ("annual", "Annual")], default="monthly")
    manager = models.CharField(max_length=255, blank=True, default="")
    active = models.BooleanField(default=False)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class ExpenseReport(models.Model):
    title = models.CharField(max_length=255)
    submitted_by = models.CharField(max_length=255, blank=True, default="")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    items_count = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[("draft", "Draft"), ("submitted", "Submitted"), ("approved", "Approved"), ("rejected", "Rejected")], default="draft")
    period = models.CharField(max_length=255, blank=True, default="")
    submitted_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
