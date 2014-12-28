from django.db import models


class Content(models.Model):
    pid       = models.IntegerField(blank=True, null=True)
    pid_index = models.IntegerField(blank=True, null=True, db_index=True)
    name = models.CharField(blank=True, null=True, max_length=100)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField('Tag', through='ContentTag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Data(models.Model):
    parent = models.OneToOneField('Content', related_name='data')
    data = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    col1  = models.CharField(blank=True, null=True, max_length=100)
    col2  = models.CharField(blank=True, null=True, max_length=100)
    col3  = models.CharField(blank=True, null=True, max_length=100)
    col4  = models.CharField(blank=True, null=True, max_length=100)
    col5  = models.CharField(blank=True, null=True, max_length=100)
    col6  = models.CharField(blank=True, null=True, max_length=100)
    col7  = models.CharField(blank=True, null=True, max_length=100)
    col8  = models.CharField(blank=True, null=True, max_length=100)
    col9  = models.CharField(blank=True, null=True, max_length=100)
    col10 = models.CharField(blank=True, null=True, max_length=100)
    col11 = models.CharField(blank=True, null=True, max_length=100)
    col12 = models.CharField(blank=True, null=True, max_length=100)
    col13 = models.CharField(blank=True, null=True, max_length=100)
    col14 = models.CharField(blank=True, null=True, max_length=100)
    col15 = models.CharField(blank=True, null=True, max_length=100)
    col16 = models.CharField(blank=True, null=True, max_length=100)


class Tag(models.Model):
    LABEL_CHOICES = (
        ('label-1', 'label-1'),
        ('label-2', 'label-2'),
        ('label-3', 'label-3'),
        ('label-4', 'label-4'),
        ('label-5', 'label-5'),
    )
    LABEL_NUM_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    tag             = models.CharField(max_length=100, db_index=True)
    label           = models.CharField(max_length=100, choices=LABEL_CHOICES)
    label_index     = models.CharField(max_length=100, choices=LABEL_CHOICES, db_index=True)
    label_num       = models.PositiveSmallIntegerField(choices=LABEL_NUM_CHOICES)
    label_num_index = models.PositiveSmallIntegerField(choices=LABEL_NUM_CHOICES, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ContentTag(models.Model):
    content = models.ForeignKey('Content')
    tag = models.ForeignKey('Tag')
