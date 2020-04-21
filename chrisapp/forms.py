from django import forms
from django.forms import ModelForm, Textarea
from .models import  Joke

class JokeForm(ModelForm):
    class Meta:
        model = Joke
        fields = ['joke_text', 'punchline_text']
        labels = {
           'joke_text' : '', 
           'punchline_text' : ''    
        }
    
        widgets = {  'joke_text' : Textarea(attrs={'cols': 80, 'rows': 1, 'placeholder': 'Your joke',  'class' : 'formFields'}),
                    'punchline_text' : Textarea(attrs={'cols': 80, 'rows': 1, 'placeholder': 'and the punchline', 'class' : 'formFields'})}


class EmailForm(forms.Form):
    your_email = forms.EmailField(label='Your email', max_length=70)