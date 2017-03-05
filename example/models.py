from django.db import models
from django.utils import timezone

from edc_base.model_mixins import BaseUuidModel
from edc_timepoint.model_mixins import TimepointModelMixin, TimepointLookupModelMixin
from edc_timepoint.timepoint_lookup import TimepointLookup


class ExampleModel(TimepointModelMixin, BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=25,
        default='123456789-0')

    report_datetime = models.DateTimeField(
        default=timezone.now)

    example_status = models.CharField(
        max_length=25,
        default='start')

    class Meta:
        app_label = 'example'


class Visit(BaseUuidModel, models.Model):

    example_model = models.ForeignKey(ExampleModel)

    report_datetime = models.DateTimeField(
        default=timezone.now)

    class Meta:
        app_label = 'example'


class CrfModel(TimepointLookupModelMixin, BaseUuidModel):

    timepoint_lookup = TimepointLookup(
        'example.examplemodel', 'visit__example_model__timepoint_status')

    visit = models.ForeignKey(Visit)

    report_datetime = models.DateTimeField(
        default=timezone.now)

    class Meta:
        app_label = 'example'
