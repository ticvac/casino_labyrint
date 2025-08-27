from django.template.response import TemplateResponse
from .models import *
from django.http import HttpResponse
from django.shortcuts import redirect
import math # lol really needed
from .utils import *



def index(request):
    args = {}
    user = request.user

    if user.is_authenticated:
        args['visits'] = PointVisit.objects.filter(user=user)
    else:
        return HttpResponse("You must be logged in to view this page.")
    # balance calculation
    transactions = user.transactions.all()
    if transactions:
        args['balance'] = transactions[0].balance_after
    else:
        args['balance'] = 0

    return TemplateResponse(request, 'game/master.html', args)


def visit_point(request, point_id):
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to visit a point.")
    user = request.user

    try:
        point = GraphPoint.objects.get(identifier=point_id)
    except GraphPoint.DoesNotExist:
        return HttpResponse("Point does not exist.")

    # get previous point
    if user.visits.filter(type=PointVisit.Type.SUCCESS).exists():
        previous_visit = user.visits.filter(type=PointVisit.Type.SUCCESS)[0]
        # on same point
        if point == previous_visit.point:
            add_message_on_staying_on_point(user, point)
            return redirect('index')
        # check if point is reachable
        if point not in previous_visit.point.next_points.all():
            add_message_on_unreachable_point(user, point)
            return redirect('index')


    # Create a visit record
    visit = PointVisit.objects.create(
        point=point,
        user=user,
        type=PointVisit.Type.SUCCESS,
    )
    # Calculate balance
    transactions = user.transactions.all()
    balance = 0
    for tx in transactions:
        balance += tx.amount
    # new diff
    string_to_eval = point.eval_string.replace("x", str(balance))
    value = eval(string_to_eval)
    balance_after = float(balance) + float(value)
    # Create a transaction record
    Transaction.objects.create(user=user, amount=value, visit=visit, balance_after=balance_after)

    return redirect('index')


def graph(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponse("You must be an admin to view this page.")
    return TemplateResponse(request, 'game/graph.html', {})