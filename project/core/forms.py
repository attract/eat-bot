from django import forms
from django.conf import settings
from core.bl.point import check_point_is_default
from core.bl.utils_helper import prn

from users.widgets import AddressAutocompleteWidget
from django.utils.translation import ugettext as _
import googlemaps


class AddressForm(forms.ModelForm):
    # https://github.com/googlemaps/google-maps-services-python
    # Look up an address with reverse geocoding
    # reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))

    address = forms.CharField(widget=AddressAutocompleteWidget, required=False, label=_('Address'))

    def clean(self, address_field='address', address_readonly=False, options={}):
        cleaned_data = self.cleaned_data
        address = self.cleaned_data.get(address_field, '')
        form_latitude = float(self.cleaned_data.get('latitude'))
        form_longitude = float(self.cleaned_data.get('longitude'))

        # if location is default, show error
        is_field_with_map = options['is_field_with_map'] if 'is_field_with_map' in options else True
        point_error = check_point_is_default(self.cleaned_data, is_field_with_map)

        if address_readonly:
            return cleaned_data

        if not address:
            self._errors[address_field] = self.error_class(['This field is required.'])
            return cleaned_data

        if address and point_error:
            self._errors[address_field] = self.error_class([point_error])
            return cleaned_data
        gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
        # Geocoding an address
        try:
            geocode_result = gmaps.geocode(address)
        except googlemaps.exceptions.HTTPError:
            self._errors[address_field] = self.error_class(
                ["Can't validate address"])
            return cleaned_data

        api_latitude = 0
        api_longitude = 0
        if len(geocode_result):
            api_latitude = geocode_result[0]['geometry']['location']['lat']
            api_longitude = geocode_result[0]['geometry']['location']['lng']

        if form_latitude - api_latitude > 0.01 or form_longitude - api_longitude > 0.01:
            self._errors[address_field] = self.error_class(
                ['Address or point on the map is not valid, please check it again.'])

        return cleaned_data
