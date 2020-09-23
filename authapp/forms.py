import django.forms as forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, \
    PasswordChangeForm

from authapp.models import ShopUser


class CleanAgeMixin:
    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Вы слишком молоды!')
        return data


class ShopUserAuthenticationForm(AuthenticationForm):
    # redirect_url = forms.HiddenInput()

    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # для возврата на страницу покупки, после логина при покупке товара
        # if 'next' in self.cleaned_data.keys():  # Не находит атрибут cleaned_data, оставил так же:
        if 'next' in self.data.keys():
            # Не понял как с помощью initial сделать вывод:
            # self.redirect_url.attrs['name'] = 'redirect_url'
            # self.redirect_url.attrs['value'] = self.data['next']
            # print(self.initial)
            # self.initial.update({'redirect_url': self.redirect_url.render})
            # Оставил сво вариант:
            self.redirect_url = forms.HiddenInput()\
                .render(name='redirect_url', value=self.data['next'])

        print(self.fields.items())
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'

            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'введите имя'
            elif field_name == 'password':
                field.widget.attrs['placeholder'] = 'введите пароль'


class ShopUserRegisterForm(UserCreationForm, CleanAgeMixin):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            # field.help_text = ''  # очистка стандартного справочного текста (слишком громоздкий)

            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'введите имя'
                field.help_text = '* обязательное поле'
                field.label += '*'
            elif field_name == 'password1' or field_name == 'password2':
                field.widget.attrs['placeholder'] = 'введите пароль'
                field.help_text = '* обязательное поле'
                field.label += '*'
            elif field_name == 'age':
                field.widget.attrs['placeholder'] = 'введите Ваш возраст'
                field.help_text = '* обязательное поле'
                field.label += '*'


class ShopUserProfileForm(UserChangeForm, CleanAgeMixin):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            field.help_text = ''

            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'введите имя'
            elif field_name == 'password':
                field.widget = forms.HiddenInput()


class ShopUserPasswordEditForm(PasswordChangeForm):
    class Meta:
        model = ShopUser
        fields = ("old_password", "new_password1", "new_password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            field.help_text = ''

            if field_name == 'old_password':
                field.widget.attrs['placeholder'] = 'введите старый пароль'
            elif field_name == 'new_password1':
                field.widget.attrs['placeholder'] = 'введите новый пароль'
            elif field_name == 'new_password2':
                field.widget.attrs['placeholder'] = 'подтвердите новый пароль'
