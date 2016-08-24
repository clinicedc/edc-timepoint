from django.db import models
from django.utils import timezone

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_timepoint.model_mixins import TimepointStatusMixin


class ExampleModel(TimepointStatusMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(
        default=timezone.now)

    example_status = models.CharField(
        max_length=25,
        default='start')

    class Meta:
        app_label = 'example'
