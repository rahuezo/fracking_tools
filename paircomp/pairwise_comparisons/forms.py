from django import forms


class DocumentForm(forms.Form):
    doc_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'accept': '.txt, .csv'}),
        label='Select a File',
        help_text='only .pdf or .txt allowed'
    )

    csv_file = forms.FileField(
        label='Select a .csv File',
        help_text='only .csv allowed',
    )
