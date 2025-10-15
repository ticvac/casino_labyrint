from django.db import models
from django.contrib.auth.models import User



class Game(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

class GraphPoint(models.Model):
    identifier = models.CharField(max_length=100, unique=True)
    next_points = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='previous_points')
    default_name = models.CharField(max_length=255, blank=True, null=True)
    eval_string_1 = models.TextField(default="0")  # string to eval, x is current balance
    message_1 = models.TextField(default="", blank=True)
    eval_string_2 = models.TextField(default="0")  # string to eval, x is current balance
    message_2 = models.TextField(default="", blank=True)
    eval_string_3 = models.TextField(default="0")  # string to eval, x is current balance
    message_3 = models.TextField(default="", blank=True)
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='graph_points')

    # random ass go
    welcome_message = models.TextField(default="", blank=True)
    opt_1_message = models.TextField(default="", blank=True)
    opt_2_message = models.TextField(default="", blank=True)
    opt_3_message = models.TextField(default="", blank=True)

    def __str__(self):
        return str(self.id) + " - " + self.identifier

    def get_str_message(self):
        m = "<br><b>"
        m += self.welcome_message + "</b>"
        point_points = self.next_points.all()
        if len(point_points) > 0:
            m += "<br>Možnosti:"
            m += f"<br>1. {self.opt_1_message} => {point_points[0].default_name}"
        if len(point_points) > 1:
            m += f"<br>2. {self.opt_2_message} => {point_points[1].default_name}"
        if len(point_points) > 2:
            m += f"<br>3. {self.opt_3_message} => {point_points[2].default_name}"
        return m


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
    amount = models.DecimalField(max_digits=1000, decimal_places=2)
    balance_after = models.DecimalField(max_digits=1000, decimal_places=2)
    visit = models.OneToOneField(PointVisit, on_delete=models.CASCADE, related_name='transaction')

    class Meta:
        ordering = ['-visit__visit_time']

    def __str__(self):
        return f"{self.user.username} - {self.amount} at {self.visit.visit_time}"


# hot fix
class ReachedZero(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reached_zero')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reached zero at {self.time}"