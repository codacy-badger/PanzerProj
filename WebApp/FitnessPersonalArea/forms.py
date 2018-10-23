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

# форма для загрузки проекционных фото пользователя
class NewProjectionPhotoForm(forms.Form):
    # projection type
    front_view_photo = "FRT"
    side_first_view_photo = "SD1"
    side_second_view_photo = "SD2"
    back_view_photo = "BCK"

    projection_view_type = forms.ChoiceField(label=_('Выберите вид к которому относится фото'),
                                             widget = forms.Select(attrs = {'class': 'form-control'}),
                                             choices = (
                                                        (front_view_photo, _('Передний вид')),
                                                        (side_first_view_photo, _('Боковой вид №1')),
                                                        (side_second_view_photo, _('Боковой вид №2')),
                                                        (back_view_photo, _('Задний вид')),
                                                        )
                                            )
    # фото проекции
    projection_view_photo = forms.ImageField(label=_("Выберите изображение"),
                                             widget = forms.ClearableFileInput(attrs = {'class': 'form-control',
                                                                                        'type':'file'}))

    projection_view_description = forms.CharField(label=_('Описание'), max_length=100, required=False,
                                                  widget = forms.Textarea(attrs = {'class': 'form-control',
                                                                                    'rows': "5" 
                                                                                  }
                                                                         )
                                                 )
