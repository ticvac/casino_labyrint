from django.template.response import TemplateResponse
from .models import *
from django.http import HttpResponse
from django.shortcuts import redirect
import math # lol really needed
from .utils import *
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET
from django.db import transaction



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
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponse("You must be a super admin to view this page.")
    return TemplateResponse(request, 'game/graph.html', {})


# --- random code XD --- lol should be secured, but whatever...
@require_GET
def graph_json(request):
    nodes = []
    edges = []
    # načti uzly a hrany jako dříve
    for p in GraphPoint.objects.all():
        nodes.append({
            'id': p.identifier,
            'label': p.default_name or p.identifier,
            'x': float(p.x),
            'y': float(p.y),
            # visits budou doplněny níže
        })
        for q in p.next_points.all():
            edges.append({'from': p.identifier, 'to': q.identifier})

    # map id -> node dict pro pohodlné doplnění visits
    node_map = {n['id']: n for n in nodes}

    # vyber návštěvy (můžeš omezit množství pokud jich je moc)
    visits_qs = PointVisit.objects.select_related('user', 'point').order_by('-visit_time')
    for v in visits_qs:
        if v.type != PointVisit.Type.SUCCESS:
            continue
        pid = v.point.identifier
        if pid not in node_map:
            continue
        node_map[pid].setdefault('visits', [])
        node_map[pid]['visits'].append({
            'user': {'id': v.user.id, 'username': v.user.username},
            'visit_time': v.visit_time.isoformat(),
            'type': int(v.type),
            'message': v.message or ''
        })

    return JsonResponse({'nodes': nodes, 'edges': edges})


@require_POST
def graph_save(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception:
        return HttpResponseBadRequest('Invalid JSON')
    nodes = payload.get('nodes', [])
    edges = payload.get('edges', [])
    # save inside transaction
    with transaction.atomic():
        # create or update nodes
        instances = {}
        for n in nodes:
            ident = n.get('id')
            if not ident: continue
            obj, created = GraphPoint.objects.get_or_create(
                identifier=ident,
                game=Game.objects.first()
            )
            obj.default_name = n.get('label') or ident
            obj.x = float(n.get('x') or 0)
            obj.y = float(n.get('y') or 0)
            obj.save()
            instances[ident] = obj
        # clear all next_points to set edges exactly as given
        # (alternatively: be incremental)
        GraphPoint.objects.update()  # noop but ensures model imported
        for obj in instances.values():
            obj.next_points.clear()
        # add edges
        for e in edges:
            f = e.get('from'); t = e.get('to')
            if f in instances and t in instances:
                instances[f].next_points.add(instances[t])
    return JsonResponse({'status': 'ok'})