from django import forms


class CsvForm(forms.Form):
    csv_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'accept': '.csv'}),
    )
