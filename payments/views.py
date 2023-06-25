from django.shortcuts import render, redirect

from payments.forms import ExpenseGroupAdd, ExpenseItemAdd
from payments.models import ExpenseGroup, ExpensesItem


def ExpensesGroupView(request):
    expense_groups = ExpenseGroup.objects.all()

    if request.method == 'POST':
        form = ExpenseGroupAdd(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('expenses_group')
            except:
                form.add_error(None, 'Data save error')
    else:
        form = ExpenseGroupAdd()

    context = {'form': form,
               'expense_groups': expense_groups}

    return render(request, 'payments/expenses_group.html', context=context)


def ExpensesItemView(request):
    expense_items = ExpensesItem.objects.all()

    if request.method == 'POST':
        form = ExpenseItemAdd(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('expenses_item')
            except:
                form.add_error(None, 'Data save error')
    else:
        form = ExpenseItemAdd()

    context = {'form': form,
               'expense_items': expense_items}

    return render(request, 'payments/expenses_item.html', context=context)


def PaymentsView(request):
    return render(request, 'payments/payments.html')


def PaymentsPlanView(request):
    return render(request, 'payments/payments_plan.html')
