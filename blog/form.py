from django import forms
from .models import CommentModel


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        exclude = ['post']
        labels = {
            'user_name': 'Your Name',
            'user_email': 'Email',
            'text': 'Comment'
        }
