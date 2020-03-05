from django.forms import ModelForm
from .models import Thread, Post
from django import forms



class NewTopicForm(ModelForm):
    message = forms.CharField(widget=forms.Textarea(
            attrs ={'rows':5, 'placeholder': 'what is on your mind?'}
    ),max_length=400,
    help_text ='The max length of the text is 4000')
    image = forms.ImageField( required = False)


    class Meta:
        model = Thread
        fields = ['title', 'message','image']



class TopicReply(ModelForm):

    class Meta:
        model = Post
        fields = ['message','image']

class UpdateForm(ModelForm):

    class Meta:
        model = Post
        fields = ['message','image']
