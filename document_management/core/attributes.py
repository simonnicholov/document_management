from django import forms


def get_select_attribute():
    return forms.Select(attrs={'class': 'form-control select2', 'data-toggle': 'select2'})
