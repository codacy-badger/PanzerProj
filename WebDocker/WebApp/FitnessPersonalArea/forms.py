from django.contrib.gis import forms


# форма для создания нового зала
class NewGym(forms.Form):
    # gym user name
    gym_name = ''
    # gym user description
    gym_description = ''
    # gym adress destination
    gym_destination = ''
    # gym geolocation
    gym_geo = forms.PointField(widget=forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))