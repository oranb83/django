from geopy.geocoders import Nominatim
from collections import namedtuple
import requests


class GeoCalculation(object):

    def get_coordinates(self, data):
        "Get coordinates"
        country = data['country']
        location = namedtuple('Location', ['street', 'city', 'country'])

        # Origin Location
        origin = location(data['origin_street'], data['origin_city'], country)
        address = self._create_address(origin)
        latitude, longitude = self._convert_address_to_coordinates(address)
        coordinates = {'start_lat': latitude, 'start_lng': longitude}

        # Destination Location
        destination = location(data['destination_street'], data['destination_city'], country)
        address = self._create_address(destination)
        latitude, longitude = self._convert_address_to_coordinates(address)
        coordinates.update({'end_lat': latitude, 'end_lng': longitude})

        return coordinates

    def _create_address(self, data):
        "Build the address string"
        address = ' '
        address = address.join(data).strip()

        return address

    def _convert_address_to_coordinates(self, address):
        "Transform address to coordinates"
        if address is None:
            return None, None

        geolocator = Nominatim()
        location = geolocator.geocode(address)
        # Geo coding can sometimes fail!
        latitude = getattr(location, 'latitude', None)
        longitude = getattr(location, 'longitude', None)

        return latitude, longitude


class Price(object):
    url = 'https://api.lyft.com/v1/cost'

    def __init__(self, coordinates):
        self.params = coordinates

    def create_result(self):
        response = self._get_cost_from_lyft()

        result = []
        for item in response['cost_estimates']:
            display_name = 'After {}'.format(item['display_name'])
            currency_code = item['currency']
            estimate = item['estimated_cost_cents_max']
            if estimate is not None:
                estimate = round(estimate * 0.75 / 100, 2)

            result.append(
                {'car type': display_name, 'currency': currency_code,
                 'estimate': estimate})

        return result

    def _get_cost_from_lyft(self):
        token = Auth().get_token()
        headers = {'Authorization': token}

        return requests.get(self.url, params=self.params, headers=headers).json()


class Auth(object):
    client_id = '5QGl6XoqSdpV'
    client_secret = '4h4FgnFeZS4tbdKHYCDy0a9iTanl4ezV'
    url = 'https://{}:{}@api.lyft.com/oauth/token'.format(client_id, client_secret)

    def get_token(self):
        "create access token"
        data = '{"grant_type": "client_credentials"}'
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
        }
        response = requests.post(self.url, data=data, headers=headers).json()
        token = '{} {}'.format(response['token_type'], response['access_token'])

        return token
