# Generated by Django 5.0.4 on 2024-05-06 03:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('employees', models.ManyToManyField(related_name='employees', to=settings.AUTH_USER_MODEL)),
                ('responsible_employee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='KPI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('total_ball', models.PositiveIntegerField()),
                ('responsible_employee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('ball', models.PositiveIntegerField()),
                ('deadline', models.DateField()),
                ('kpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metrics', to='dashboard.kpi')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='dashboard.metric')),
            ],
        ),
        migrations.CreateModel(
            name='Notefication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(choices=[(1, "Rag'batlantirish"), (2, "Ma'lumot berish"), (3, 'Tanqid qilish'), (4, 'Ogohlantirish')], default=1)),
                ('massage', models.TextField()),
                ('unread', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notefications', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='submissions')),
                ('comment', models.TextField()),
                ('ball', models.PositiveIntegerField(blank=True)),
                ('submitted_at', models.DateTimeField(auto_now=True)),
                ('is_checked', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to=settings.AUTH_USER_MODEL)),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='works', to=settings.AUTH_USER_MODEL)),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='dashboard.metric')),
            ],
            options={
                'unique_together': {('metric', 'employee')},
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ball', models.PositiveIntegerField()),
                ('comment', models.TextField()),
                ('marked_at', models.DateTimeField(auto_now=True)),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='marks', to=settings.AUTH_USER_MODEL)),
                ('submission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mark', to='dashboard.submission')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_ball', models.PositiveIntegerField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to=settings.AUTH_USER_MODEL)),
                ('kpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.kpi')),
            ],
            options={
                'unique_together': {('kpi', 'employee')},
            },
        ),
    ]
