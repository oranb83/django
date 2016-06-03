from django import forms


class GeoForm(forms.Form):
    country = forms.CharField(max_length=255, required=True)
    origin_city = forms.CharField(max_length=255, required=True)
    origin_street = forms.CharField(max_length=255, required=True)
    destination_city = forms.CharField(max_length=255, required=True)
    destination_street = forms.CharField(max_length=255, required=True)
