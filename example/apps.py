from django.apps import AppConfig as DjangoAppConfig

from edc_timepoint_status.apps import AppConfig as EdcTimepointStatusAppConfigParent


class AppConfig(DjangoAppConfig):
    name = 'example'


class EdcTimepointStatusAppConfig(EdcTimepointStatusAppConfigParent):
    timepoint_models = {
        'example.appointment': {
            'datetime_field': 'appt_datetime',  # the datetime field
            'status_field': 'appt_status',  # the status field
            'closed_status': 'CLOSED'  # the value of appt_status when closed
        }
    }
