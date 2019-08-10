from django.contrib.auth.forms import PasswordChangeForm as AuthPasswordChangeForm


class PasswordChangeForm(AuthPasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password2'].label = 'Confirm password'
