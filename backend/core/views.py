import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Expense, ExpenseCategory, ExpenseReport


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['expense_count'] = Expense.objects.count()
    ctx['expense_travel'] = Expense.objects.filter(category='travel').count()
    ctx['expense_food'] = Expense.objects.filter(category='food').count()
    ctx['expense_office'] = Expense.objects.filter(category='office').count()
    ctx['expense_total_amount'] = Expense.objects.aggregate(t=Sum('amount'))['t'] or 0
    ctx['expensecategory_count'] = ExpenseCategory.objects.count()
    ctx['expensecategory_monthly'] = ExpenseCategory.objects.filter(period='monthly').count()
    ctx['expensecategory_quarterly'] = ExpenseCategory.objects.filter(period='quarterly').count()
    ctx['expensecategory_annual'] = ExpenseCategory.objects.filter(period='annual').count()
    ctx['expensecategory_total_budget'] = ExpenseCategory.objects.aggregate(t=Sum('budget'))['t'] or 0
    ctx['expensereport_count'] = ExpenseReport.objects.count()
    ctx['expensereport_draft'] = ExpenseReport.objects.filter(status='draft').count()
    ctx['expensereport_submitted'] = ExpenseReport.objects.filter(status='submitted').count()
    ctx['expensereport_approved'] = ExpenseReport.objects.filter(status='approved').count()
    ctx['expensereport_total_total'] = ExpenseReport.objects.aggregate(t=Sum('total'))['t'] or 0
    ctx['recent'] = Expense.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def expense_list(request):
    qs = Expense.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(category=status_filter)
    return render(request, 'expense_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def expense_create(request):
    if request.method == 'POST':
        obj = Expense()
        obj.title = request.POST.get('title', '')
        obj.category = request.POST.get('category', '')
        obj.amount = request.POST.get('amount') or 0
        obj.date = request.POST.get('date') or None
        obj.submitted_by = request.POST.get('submitted_by', '')
        obj.status = request.POST.get('status', '')
        obj.receipt_url = request.POST.get('receipt_url', '')
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/expenses/')
    return render(request, 'expense_form.html', {'editing': False})


@login_required
def expense_edit(request, pk):
    obj = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '')
        obj.category = request.POST.get('category', '')
        obj.amount = request.POST.get('amount') or 0
        obj.date = request.POST.get('date') or None
        obj.submitted_by = request.POST.get('submitted_by', '')
        obj.status = request.POST.get('status', '')
        obj.receipt_url = request.POST.get('receipt_url', '')
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/expenses/')
    return render(request, 'expense_form.html', {'record': obj, 'editing': True})


@login_required
def expense_delete(request, pk):
    obj = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/expenses/')


@login_required
def expensecategory_list(request):
    qs = ExpenseCategory.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(period=status_filter)
    return render(request, 'expensecategory_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def expensecategory_create(request):
    if request.method == 'POST':
        obj = ExpenseCategory()
        obj.name = request.POST.get('name', '')
        obj.budget = request.POST.get('budget') or 0
        obj.spent = request.POST.get('spent') or 0
        obj.period = request.POST.get('period', '')
        obj.manager = request.POST.get('manager', '')
        obj.active = request.POST.get('active') == 'on'
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/expensecategories/')
    return render(request, 'expensecategory_form.html', {'editing': False})


@login_required
def expensecategory_edit(request, pk):
    obj = get_object_or_404(ExpenseCategory, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.budget = request.POST.get('budget') or 0
        obj.spent = request.POST.get('spent') or 0
        obj.period = request.POST.get('period', '')
        obj.manager = request.POST.get('manager', '')
        obj.active = request.POST.get('active') == 'on'
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/expensecategories/')
    return render(request, 'expensecategory_form.html', {'record': obj, 'editing': True})


@login_required
def expensecategory_delete(request, pk):
    obj = get_object_or_404(ExpenseCategory, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/expensecategories/')


@login_required
def expensereport_list(request):
    qs = ExpenseReport.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'expensereport_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def expensereport_create(request):
    if request.method == 'POST':
        obj = ExpenseReport()
        obj.title = request.POST.get('title', '')
        obj.submitted_by = request.POST.get('submitted_by', '')
        obj.total = request.POST.get('total') or 0
        obj.items_count = request.POST.get('items_count') or 0
        obj.status = request.POST.get('status', '')
        obj.period = request.POST.get('period', '')
        obj.submitted_date = request.POST.get('submitted_date') or None
        obj.save()
        return redirect('/expensereports/')
    return render(request, 'expensereport_form.html', {'editing': False})


@login_required
def expensereport_edit(request, pk):
    obj = get_object_or_404(ExpenseReport, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '')
        obj.submitted_by = request.POST.get('submitted_by', '')
        obj.total = request.POST.get('total') or 0
        obj.items_count = request.POST.get('items_count') or 0
        obj.status = request.POST.get('status', '')
        obj.period = request.POST.get('period', '')
        obj.submitted_date = request.POST.get('submitted_date') or None
        obj.save()
        return redirect('/expensereports/')
    return render(request, 'expensereport_form.html', {'record': obj, 'editing': True})


@login_required
def expensereport_delete(request, pk):
    obj = get_object_or_404(ExpenseReport, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/expensereports/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['expense_count'] = Expense.objects.count()
    data['expensecategory_count'] = ExpenseCategory.objects.count()
    data['expensereport_count'] = ExpenseReport.objects.count()
    return JsonResponse(data)
