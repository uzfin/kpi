from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from dashboard.models import Submission, Mark


@receiver(post_save, sender=Submission)
def submission_post_save(sender, instance, created, **kwargs):
    if created:
        mark = Mark.objects.create(
            ball=instance.metric.ball,
            comment="",
            submission=instance,
        )

    else:
        mark = instance.mark
        mark.ball = instance.ball
