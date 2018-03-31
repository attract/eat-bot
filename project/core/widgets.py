from datetime import date, datetime, time
from django import forms
from django.conf import settings
from django.forms import ClearableFileInput
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail
from suit.widgets import HTML5Input

from core.bl.datetime_helper import get_date_text
from core.bl.utils_helper import prn


class HTML5SplitDateTimeWidget(forms.SplitDateTimeWidget):
    def __init__(self, attrs=None):
        widgets = (HTML5Input(input_type='date', ), HTML5Input(input_type='time'))
        forms.MultiWidget.__init__(self, widgets, attrs)


class PhotoWidget(forms.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        """
        Widget for show photo
        """
        context = self.get_context(name, value, attrs)
        context['widget']['value'] = value
        context['widget']['value_full'] = "%s%s%s" % (settings.SITE_URL,
                                                      settings.MEDIA_URL,
                                                      context['widget']['value'])

        return render_to_string('widgets/photo_widget.html', context)


class DatePickerWidget(forms.Widget):
    template_name = 'widgets/date_picker_formatted.html'

    def render(self, name, value, attrs=None, renderer=None):
        label = ''
        attrs['value_picker'] = get_date_text(value)
        return mark_safe(render_to_string(self.template_name, {
            'label': label,
            'name': name,
            'value': value,
            'attrs': attrs,
        }))


class PhoneNumberFormattedWidget(forms.Widget):
    template_name = 'widgets/phone_number_formatted.html'

    def render(self, name, value, attrs=None, renderer=None):
        label = ''
        attrs['value_picker'] = value

        return mark_safe(render_to_string(self.template_name, {
            'label': label,
            'name': name,
            'value': value,
            'attrs': attrs,
        }))


class JqueryTimePickerWidget(forms.Widget):
    template_name = 'widgets/jquery_time_picker_widget.html'

    def render(self, name, value, attrs=None, renderer=None):
        label = ''
        # attrs['value_picker'] = get_date_text(value)

        if value:
            if isinstance(value, time):
                value = value.strftime("%H:%M")
            else:
                pass

        return mark_safe(render_to_string(self.template_name, {
            'label': label,
            'name': name,
            'value': value,
            'attrs': attrs,
        }))


class ClearableFileInputCustom(ClearableFileInput):
    #template_name = 'django/forms/widgets/clearable_file_input.html'
    template_name = 'widgets/clearable_file_input.html'

    def _render(self, template_name, context, renderer=None):
        return mark_safe(render_to_string(template_name, context))
