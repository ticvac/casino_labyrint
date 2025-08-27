from .models import *

def add_message_on_staying_on_point(user, point):
    PointVisit.objects.create(
        point=point,
        user=user,
        type=PointVisit.Type.BROKE_RULE,
        message="You stayed on the same point without moving."
    )


def add_message_on_unreachable_point(user, point):
    PointVisit.objects.create(
        point=point,
        user=user,
        type=PointVisit.Type.BROKE_RULE,
        message="You tried to visit an unreachable point."
    )