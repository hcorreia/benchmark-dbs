# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pid', models.IntegerField(null=True, blank=True)),
                ('pid_index', models.IntegerField(db_index=True, null=True, blank=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContentTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.ForeignKey(to='app.Content')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('col1', models.CharField(max_length=100, null=True, blank=True)),
                ('col2', models.CharField(max_length=100, null=True, blank=True)),
                ('col3', models.CharField(max_length=100, null=True, blank=True)),
                ('col4', models.CharField(max_length=100, null=True, blank=True)),
                ('col5', models.CharField(max_length=100, null=True, blank=True)),
                ('col6', models.CharField(max_length=100, null=True, blank=True)),
                ('col7', models.CharField(max_length=100, null=True, blank=True)),
                ('col8', models.CharField(max_length=100, null=True, blank=True)),
                ('col9', models.CharField(max_length=100, null=True, blank=True)),
                ('col10', models.CharField(max_length=100, null=True, blank=True)),
                ('col11', models.CharField(max_length=100, null=True, blank=True)),
                ('col12', models.CharField(max_length=100, null=True, blank=True)),
                ('col13', models.CharField(max_length=100, null=True, blank=True)),
                ('col14', models.CharField(max_length=100, null=True, blank=True)),
                ('col15', models.CharField(max_length=100, null=True, blank=True)),
                ('col16', models.CharField(max_length=100, null=True, blank=True)),
                ('parent', models.OneToOneField(related_name='data', to='app.Content')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=100, db_index=True)),
                ('label', models.CharField(max_length=100, choices=[(b'label-1', b'label-1'), (b'label-2', b'label-2'), (b'label-3', b'label-3'), (b'label-4', b'label-4'), (b'label-5', b'label-5')])),
                ('label_index', models.CharField(db_index=True, max_length=100, choices=[(b'label-1', b'label-1'), (b'label-2', b'label-2'), (b'label-3', b'label-3'), (b'label-4', b'label-4'), (b'label-5', b'label-5')])),
                ('label_num', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('label_num_index', models.PositiveSmallIntegerField(db_index=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contenttag',
            name='tag',
            field=models.ForeignKey(to='app.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='tags',
            field=models.ManyToManyField(to='app.Tag', through='app.ContentTag'),
            preserve_default=True,
        ),
    ]
