# edc-timepoint

Lock a "timepoint" from further editing once data is cleaned and reviewed

With module `edc_timepoint` a data manager or supervisor is able to flag a model instance, that represents a timepoint, as closed to further edit. A good candidate for a "timepoint" model is one that is used to cover other data collection, such as an appointment. An appointment can be referred to by forms for all data collected during the appointment. If the appointment is closed to further edit so are all the data collected during that appointment. 


### Install

    pip install git+https://github.com/botswana-harvard/edc-timepoint@develop#egg=edc-timepoint
    
### Usage
    
Select a model that represent a timepoint. The model should at least have a datetime field and a `status` field. For example `Appointment`:

    APPT_STATUS = (
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
    )

    class Appointment(TimepointStatusMixin, BaseUuidModel):
    
        appt_datetime = models.DateTimeField(
            verbose_name='Appointment date and time')

        appt_status = models.CharField(
            verbose_name='Status',
            choices=APPT_STATUS,
            max_length=25,
            default='OPEN')
        class Meta:
            app_label = 'example'

The `TimepointStatusMixin` adds fields and methods prefixed as `timepoint_<something>`. There is also a signal that is loaded in the `AppConfig.ready` that resets the timepoint attributes should the `Appointment` status change from `closed`. Only field `timepoint_status` is meant to be edited by the user.

In your projects `apps.py` subclass `edc_timepoint.apps.AppConfig` and declare `Appointment` as a timepoint model in the `timepoint_models` attribute:

    from django.apps import AppConfig as DjangoAppConfig
    from edc_timepoint.apps import AppConfig as EdcTimepointAppConfigParent
    
    class AppConfig(DjangoAppConfig):
        name = 'example'
    
    class EdcTimepointAppConfig(EdcTimepointAppConfigParent):
        timepoint_models = {
            'example.appointment': {
                'datetime_field': 'appt_datetime',  # the datetime field
                'status_field': 'appt_status',  # the status field
                'closed_status': 'CLOSED'  # the value of appt_status when closed
            }
        }
        
The user updates the `Appointment` normally closing it when the appointment is done. Then a data manager or supervisor can close the `Appointment` to further edit once the data has been reviewed.

To close the `Appointment` to further edit the code needs to call the `timepoint_close_timepoint` method:

    appointment = Appointment.objects.create(**options)
    appointment.appt_status = 'CLOSED'
    appointment.timepoint_close_timepoint()
    
If the `appointment.appt_status` is not `CLOSED` when `timepoint_close_timepoint` is called, a `TimepointStatusError` is raised.
    
If the appointment is successfully closed to further edit, any attempts to call `appointment.save()` will raise a `TimepointStatusError`.

The `Appointment` may be re-opened for edit by calling method `timepoint_open_timepoint`.



