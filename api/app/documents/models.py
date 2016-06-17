from django.db import models
from django.conf import settings
from dp_base_libs.models import DPAbstractModel, DPAbstractSignable, DPAbstractTimestampable
from django.contrib.auth.models import Group


class DocumentTemplate(DPAbstractModel, DPAbstractSignable, DPAbstractTimestampable):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(blank=True, null=True, default='')
    # owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, related_name='document_owner')
    creators_group = models.ForeignKey(Group, blank=False, related_name='group_creators') # Who can create this document

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
    template = models.ForeignKey(DocumentTemplate, null=False, blank=False, related_name='document_template_fields')
    name = models.CharField(max_length=255, null=False, blank=False)
    widget = models.CharField(max_length=50, choices=WIDGETS, default=WIDGET_STRING, help_text='field widget')

    class Meta:
        ordering = ['name']


class DocumentTemplateStep(DPAbstractModel, DPAbstractSignable, DPAbstractTimestampable):
    template = models.ForeignKey(DocumentTemplate, null=False, blank=False, related_name='document_template_steps')
    step_number = models.SmallIntegerField(null=False, blank=False, default=0)
    name = models.CharField(max_length=255, null=False, blank=False)
    members_group = models.ForeignKey(Group, blank=False, related_name='members_group')
    editable_fields = models.ManyToManyField(DocumentTemplateField, blank=True, related_name='editable_fields')
    readonly_fields = models.ManyToManyField(DocumentTemplateField, blank=True, related_name='readonly_fields')

    class Meta:
        ordering = ['step_number']


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

    template = models.ForeignKey(DocumentTemplate, blank=False, related_name='document_templates')
    name = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(max_length=50, choices=STATUSES, default=STATUS_NEW, help_text='document status')
    step = models.ForeignKey(DocumentTemplateStep, null=False, blank=False, related_name='document_step')

    class Meta:
        ordering = ['name']

    def get_first_step(self):
        step = DocumentTemplateStep.objects.filter(template_id=self.template.pk).order_by('step_number')[0]
        return step

    def get_current_step(self):
        return self.step

    def next_step(self, user):
        user_groups = [group.id for group in user.groups.all()]
        if self.step.members_group.pk in user_groups:
            next_steps = DocumentTemplateStep.objects.filter(template=self.template.pk, step_number__gt=self.step.step_number).order_by('step_number')
            if next_steps is not None and len(next_steps) > 0:
                self.step = next_steps[0]
                self.save()
                return True
            else:
                return False
        else:
            raise ValueError('You have not permission for this action')


class DocumentValues(DPAbstractModel, DPAbstractSignable, DPAbstractTimestampable):
    document = models.ForeignKey(Document, null=False, blank=False, related_name='document_values')
    field = models.ForeignKey(DocumentTemplateField, null=False, blank=False, related_name='document_field')
    value = models.TextField(blank=True, null=True, default='')


