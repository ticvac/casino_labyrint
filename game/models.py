from django.db import models
from django.contrib.auth.models import User


class GraphPoint(models.Model):
    identifier = models.CharField(max_length=100, unique=True)
    next_points = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='previous_points')
    default_name = models.CharField(max_length=255, blank=True, null=True)
    default_message = models.TextField(blank=True, null=True)
    eval_string = models.TextField()
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)

    def __str__(self):
        return self.identifier


class PointVisit(models.Model):
    class Type(models.IntegerChoices):
        SUCCESS = 1, 'Success'
        BROKE_RULE = 2, 'Broke Rule'

    point = models.ForeignKey(GraphPoint, on_delete=models.CASCADE, related_name='visits')
    visit_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visits') # lol broke 2 coherence...
    type = models.IntegerField(choices=Type.choices)
    message = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-visit_time']

    def __str__(self):
        return f"{self.user.username} visited {self.point.identifier} at {self.visit_time}"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    visit = models.OneToOneField(PointVisit, on_delete=models.CASCADE, related_name='transaction')

    class Meta:
        ordering = ['-visit__visit_time']

    def __str__(self):
        return f"{self.user.username} - {self.amount} at {self.visit.visit_time}"