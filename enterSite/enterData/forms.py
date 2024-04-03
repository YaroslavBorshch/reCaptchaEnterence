from django import forms


class GetDataByUsernameForm(forms.Form):
    username = forms.CharField(label='Username',
                               max_length=32,
                               )
    username.widget.attrs.update({
                                   'class': 'form-control',
                                   'placeholder': 'name@example.com'
                               })
