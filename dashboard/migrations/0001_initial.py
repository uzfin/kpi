# Generated by Django 5.0.4 on 2024-05-15 10:11

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
            name='KPI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('ball', models.PositiveIntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Criterion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('ball', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('responsible_person', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='criterions', to=settings.AUTH_USER_MODEL)),
                ('kpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterions', to='dashboard.kpi')),
            ],
        ),
        migrations.CreateModel(
            name='Clause',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('ball', models.PositiveIntegerField()),
                ('does_the_system_give_mark', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='dashboard.clause')),
                ('criterion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clauses', to='dashboard.criterion')),
                ('kpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clauses', to='dashboard.kpi')),
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
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='notefications', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ball', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to=settings.AUTH_USER_MODEL)),
                ('kpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='dashboard.kpi')),
            ],
            options={
                'unique_together': {('kpi', 'employee')},
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='submissions')),
                ('comment', models.TextField()),
                ('is_checked', models.BooleanField(default=False)),
                ('is_marked', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('clause', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='dashboard.clause')),
                ('kpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='dashboard.kpi')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('owner', 'clause')},
            },
        ),
    ]
