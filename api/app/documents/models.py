from django.db import models
from django.conf import settings
from dp_base_libs.models import DPAbstractModel, DPAbstractSignable, DPAbstractTimestampable


class DocumentTemplate(DPAbstractModel, DPAbstractSignable, DPAbstractTimestampable):
    name = models.CharField(max_length=255, null=False, blank=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, related_name='document_owner')
    creators = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='document_creators')  # Who can create this document

    class Meta:
        ordering = ['name']


class DocumentTemplateField(DPAbstractModel, DPAbstractSignable, DPAbstractTimestampable):
    WIDGET_STRING = 'string'
    WIDGET_TEXT = 'text'
    WIDGET_CALCULATED = 'calculated'
    WIDGETS = (
        (WIDGET_STRING,     'String'),
        (WIDGET_TEXT,       'TEXT'),
        (WIDGET_CALCULATED, 'Calculated Field')
    )
    template = models.ForeignKey(DocumentTemplate, null=False, blank=False, related_name='document_template')
    name = models.CharField(max_length=255, null=False, blank=False)
    widget = models.CharField(max_length=50, choices=WIDGETS, default=WIDGET_STRING, help_text='field widget')

    class Meta:
        ordering = ['name']


class DocumentStep(DPAbstractModel, DPAbstractSignable, DPAbstractTimestampable):
    step_number = models.SmallIntegerField(null=False, blank=False, default=0)
    name = models.CharField(max_length=255, null=False, blank=False)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='step_members')
    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='step_editors')
    viewers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='step_viewers')

    class Meta:
        ordering = ['name']


class Document(DPAbstractModel, DPAbstractSignable, DPAbstractTimestampable):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_REJECTED = 'rejected'
    STATUS_APPROVED = 'approved'
    STATUS_PAID = 'paid'
    STATUSES = (
        (STATUS_NEW, 'New'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_PAID, 'Paid')
    )

    name = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(max_length=50, choices=STATUSES, default=STATUS_NEW, help_text='document status')
    step = models.ForeignKey(DocumentStep, null=False, blank=False, related_name='document_step')

    class Meta:
        ordering = ['name']


class DocumentValues(DPAbstractModel, DPAbstractSignable, DPAbstractTimestampable):
    document = models.ForeignKey(Document, null=False, blank=False, related_name='document')
    field = models.ForeignKey(DocumentTemplateField, null=False, blank=False, related_name='document_field')
    value = models.TextField(blank=True, null=True, default='')


