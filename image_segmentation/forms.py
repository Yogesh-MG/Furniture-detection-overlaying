from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField()
    color = forms.ChoiceField(choices=[('red', 'Red'), ('green', 'Green'), ('blue', 'Blue')])
