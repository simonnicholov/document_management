from django import forms


class RequestPermissionForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea())

    def __init__(self, document, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document = document
        self.user = user

    def save(self, *args, **kwargs):
        self.document.permission_requests.create(reason=self.cleaned_data['reason'],
                                                 user=self.user)

        return self.document
