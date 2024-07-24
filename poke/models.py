from django.db import models
from django.contrib.auth.models import User

class Poke(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_pokes', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_pokes', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} poked {self.to_user}"

    class Meta:
        unique_together = ('from_user', 'to_user', 'timestamp')
