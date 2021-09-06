from django.db import models
import re, bcrypt

# Create your models here.
class UserValidation(models.Manager):
    def user_validate(self, post):
        email_ver= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors={}
        if len(post['fname'])<2 or len(post['lname'])<2:
            errors['name']='Name entry not valid!'
        if not email_ver.match(post['email']):
            errors['email']= 'Email format incorrect!'
        if len(post['pw']) ==0:
            errors['pw']='Password needed to continue!'
        elif post['pw'] != post['pw_conf']:
            errors['password']='Passwords must match!'
        return errors
    def login_validate(self, post):
        errors={}
        user_logged= User.objects.filter(email=post['email'])
        if len(post['email'])== 0:
            errors['email']='Enter an email please!'
        elif len(user_logged)==0:
            errors['dne']='No user with that email'
        if len(post['pw']) == 0:
            errors['pw']='Password needed to continue!'
        elif not bcrypt.checkpw(post['pw'].encode(), user_logged[0].pw.encode()):
            errors['incorrect']='Password/Email combination incorrect'
        return errors


class User(models.Model):
    fname= models.CharField(max_length=25)
    lname= models.CharField(max_length=25)
    email=models.CharField(max_length=50)
    pw=models.CharField(max_length=30)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserValidation()