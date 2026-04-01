from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Expense, ExpenseCategory, ExpenseReport
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusExpense with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusexpense.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Expense.objects.count() == 0:
            for i in range(10):
                Expense.objects.create(
                    title=f"Sample Expense {i+1}",
                    category=random.choice(["travel", "food", "office", "software", "equipment", "marketing"]),
                    amount=round(random.uniform(1000, 50000), 2),
                    date=date.today() - timedelta(days=random.randint(0, 90)),
                    submitted_by=f"Sample {i+1}",
                    status=random.choice(["pending", "approved", "rejected", "reimbursed"]),
                    receipt_url=f"https://example.com/{i+1}",
                    notes=f"Sample notes for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Expense records created'))

        if ExpenseCategory.objects.count() == 0:
            for i in range(10):
                ExpenseCategory.objects.create(
                    name=f"Sample ExpenseCategory {i+1}",
                    budget=round(random.uniform(1000, 50000), 2),
                    spent=round(random.uniform(1000, 50000), 2),
                    period=random.choice(["monthly", "quarterly", "annual"]),
                    manager=f"Sample {i+1}",
                    active=random.choice([True, False]),
                    description=f"Sample description for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 ExpenseCategory records created'))

        if ExpenseReport.objects.count() == 0:
            for i in range(10):
                ExpenseReport.objects.create(
                    title=f"Sample ExpenseReport {i+1}",
                    submitted_by=f"Sample {i+1}",
                    total=round(random.uniform(1000, 50000), 2),
                    items_count=random.randint(1, 100),
                    status=random.choice(["draft", "submitted", "approved", "rejected"]),
                    period=f"Sample {i+1}",
                    submitted_date=date.today() - timedelta(days=random.randint(0, 90)),
                )
            self.stdout.write(self.style.SUCCESS('10 ExpenseReport records created'))
