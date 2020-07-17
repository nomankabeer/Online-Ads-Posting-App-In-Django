from django import forms

class PostFormValidation(forms.Form):
    title = forms.CharField(min_length=10  ,  max_length=255 , required=True)
    content = forms.CharField(min_length=20 , max_length=5000 , required=True)
    cover = forms.ImageField(required=True)
    gallery = forms.ImageField(required=True)


class PostFormEditValidation(forms.Form):
    title = forms.CharField(min_length=10  ,  max_length=255 , required=True)
    content = forms.CharField(min_length=20 , max_length=5000 , required=True)