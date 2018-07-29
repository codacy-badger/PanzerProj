from django.contrib.gis import forms
from django.utils.translation import gettext_lazy as _

from .models import BodyParameter


# форма для внесения данных по параметрам пользователя
class NewParameterData(forms.Form):
    # gym user name
    user_parameter = forms.ChoiceField(label=_('Выберите параметр'),
                                       widget = forms.Select(attrs = {'class': 'main-inp wide'}),
                                       choices = [])
    # gym user description
    body_data = ''

    def __init__(self, *args, **kwargs):
        super(NewParameterData, self).__init__(*args, **kwargs)
        user_id = kwargs.pop('user_id', None)
        # получаем список всех параметров выбранного пользователя
        all_user_params = BodyParameter.objects.filter(user__user__id=user_id)
        self.fields['user_parameter'].choices = ((x.id, x.body_title) for x in all_user_params)
