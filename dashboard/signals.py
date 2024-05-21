from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from dashboard.models import Submission, Mark, Result


@receiver(post_save, sender=Submission)
def submission_post_save(sender, instance, created, **kwargs):
    if created:
        Mark.objects.create(
            submission=instance,
            criterion=instance.clause.criterion,
            employee=instance.owner,
            ball=instance.clause.ball,
            comment="",
        )

    else:
        # TODO: agar submission update qilinsa nima qilish kerak?
        pass

@receiver(post_save, sender=Mark)
def mark_post_save(sender, instance, created, **kwargs):
    kpi = instance.criterion.kpi
    employee = instance.employee

    if created: 
        try:
            result = Result.objects.get(kpi=kpi, employee=employee)
            result.ball += instance.ball
            result.save()
        except Result.DoesNotExist:
            Result.objects.create(
                kpi=kpi, 
                employee=employee,
                ball=instance.ball
            )

@receiver(pre_save, sender=Mark)
def mark_pre_save(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Mark.objects.get(pk=instance.pk)
        
        kpi = instance.criterion.kpi
        employee = instance.employee

        result = Result.objects.get(kpi=kpi, employee=employee)
        result.ball -= old_instance.ball
        result.ball += instance.ball
        result.save()

        submission = instance.submission
        submission.is_checked = True
        submission.save()
    
@receiver(pre_delete, sender=Submission)
def mark_pre_delete(sender, instance, **kwargs):
    mark = instance.mark
    mark.delete()

@receiver(pre_delete, sender=Mark)
def mark_pre_delete(sender, instance, **kwargs):
    kpi = instance.criterion.kpi
    employee = instance.employee

    result = Result.objects.get(kpi=kpi, employee=employee)
    result.ball -= instance.ball
    result.save()
