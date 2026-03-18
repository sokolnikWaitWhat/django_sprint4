from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError


class NewUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        pass

    def clean_username(self):
        username = self.cleaned_data.get('username')
        bad_simbols = './()<>:=&#*-+!{}[]"?,' + "'"
        for simbol in bad_simbols:
            if simbol in username:
                raise ValidationError(
                    'Некорректное имя пользователя, попробуйте другое '
                    + f'(без {bad_simbols}).')
        return username
