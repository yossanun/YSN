# Generated by Django 4.0.4 on 2022-05-22 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Personnel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('personnel_type', models.IntegerField(choices=[('class_teacher', 0), ('head_of_the_room', 1), ('student', 2)], default=2)),
                ('school_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apis.classes')),
            ],
        ),
        migrations.CreateModel(
            name='Schools',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentSubjectsScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit', models.IntegerField()),
                ('score', models.FloatField(default=0)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apis.personnel')),
                ('subjects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apis.subjects')),
            ],
        ),
        migrations.CreateModel(
            name='SchoolStructure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='apis.schoolstructure')),
            ],
        ),
        migrations.AddField(
            model_name='classes',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apis.schools'),
        ),
        migrations.AddConstraint(
            model_name='studentsubjectsscore',
            constraint=models.UniqueConstraint(fields=('student', 'subjects'), name='unique_subject_score'),
        ),
        migrations.AddConstraint(
            model_name='classes',
            constraint=models.UniqueConstraint(fields=('school', 'class_order'), name='unique_school_order'),
        ),
    ]
