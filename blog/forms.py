from dataclasses import fields
from .models import Comment,Post,SearchBox
from django import forms

class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('author','title','body')

        widgets = {
            'title' : forms.TextInput(attrs={'class':'textinputclass'}),
            'body' : forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }


class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ('name','email','body')

class SearchForm(forms.Form):
  query = forms.CharField()

