from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry

from core.bl.utils_helper import prn


def get_point(latitude, longitude):
    point = None
    if latitude and longitude:
        point = GEOSGeometry('POINT(%s %s)' % (longitude, latitude), srid=4326)
    return point


def check_point_is_default(cleaned_data={}, is_field_with_map=True):
    latitude = 0
    if 'latitude' in cleaned_data:
        latitude = cleaned_data.get('latitude')
    longitude = 0
    if 'longitude' in cleaned_data:
        longitude = cleaned_data.get('longitude')
    # if location default, show error
    is_error = False
    if not latitude and not longitude:
        is_error = True
    if latitude == settings.GEOLOCATION_MAP_DEFAULT['lat'] and \
                    longitude == settings.GEOLOCATION_MAP_DEFAULT['lng']:
        is_error = True
    if is_error:
        if is_field_with_map:
            return u'Location is not initiated on the map. ' \
                   u'Please, select location in dropdown list or set point on the map'
        else:
            return u'Location is not initiated on the map. ' \
                   u'Please, select location in dropdown list'
    return False
