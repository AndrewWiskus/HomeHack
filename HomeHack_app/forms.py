from django import forms
from .models import ProjectPost

class ProjectForm(forms.ModelForm): 
    class Meta: 
        model = ProjectPost 
        fields = ['title', 'content', 'tools', 'post_image', 'poster', 'created_at', 'updated_at', 'likes', 'objects'] 