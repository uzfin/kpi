from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from dashboard.models import Submission, Mark, Result


@receiver(post_save, sender=Submission)
def submission_post_save(sender, instance, created, **kwargs):
    if created:
        Mark.objects.create(
            ball=instance.metric.ball,
            comment="",
            submission=instance,
        )

    else:
        # TODO: agar submission update qilinsa nima qilish kerak?
        pass

@receiver(post_save, sender=Mark)
def mark_post_save(sender, instance, created, **kwargs):
    kpi = instance.submission.metric.kpi
    employee = instance.submission.employee

    if created: 
        try:
            result = Result.objects.get(kpi=kpi, employee=employee)
            result.total_ball += instance.ball
            result.save()
        except Result.DoesNotExist:
            Result.objects.create(
                kpi=kpi, 
                employee=employee,
                total_ball=instance.ball
            )
    
@receiver(pre_save, sender=Mark)
def mark_pre_save(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Mark.objects.get(pk=instance.pk)
        
        kpi = instance.submission.metric.kpi
        employee = instance.submission.employee

        result = Result.objects.get(kpi=kpi, employee=employee)
        result.total_ball -= old_instance.ball
        result.total_ball += instance.ball
        result.save()
