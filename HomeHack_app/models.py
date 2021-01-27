from django.db import models
import re

class UserManager(models.Manager):
    def validator(self, postdata):
        email_check=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors={}
        if len(postdata['f_n'])<2:
            errors['f_n']="First name must be longer than 2 characters"
        if len(postdata['l_n'])<2:
            errors['l_n']="Last name must be longer than 2 characters"
        if not email_check.match(postdata['email']):
            errors['email']="Email must be valid format"
        if User.objects.filter(email=postdata['email']).exists():
            errors['email']="duplicate_email"
        if "pw" in postdata:
            if len(postdata['pw'])<8:
                errors['pw']="Password must be at least 8 characters"
            if postdata['pw'] != postdata['conf_pw']:
                errors['conf_pw']="Password and confirm password must match"
        return errors


class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField(('email address'), unique=True)
    city=models.CharField(max_length=255)
    state=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()


class ProjectManager(models.Manager):
    def project_validator(self, postdata):
        errors={}
        if len(postdata['title'])<3:
            errors['title']="Title must be longer than 3 characters"
        if len(postdata['content'])<10:
            errors['content']="Content must be longer than 10 characters"
        return errors


class ProjectPost(models.Model):
    title=models.CharField(max_length=255)
    content=models.TextField()
    tools=models.TextField()
    post_image = models.ImageField(null=True, blank=True, upload_to="upload/")
    poster=models.ForeignKey(User, related_name="projects", on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    likes=models.ManyToManyField(User, related_name='like_project')
    objects=ProjectManager()


class Comment(models.Model):
    content=models.TextField()
    comment_poster=models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    message=models.ForeignKey(ProjectPost, related_name="comments", on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
