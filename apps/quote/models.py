from __future__ import unicode_literals
from django.db import models
from datetime import datetime 
import bcrypt
import re

# Regex for email validation
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Class to validate registration
class UserManager(models.Manager):
  def registor_validation(self, postData):
    
    errors = {}
    today = datetime.now()

    if len(postData['name']) < 2:
      errors['name'] = 'First name must be at least 2 charaters'
    if len(postData['alias']) < 2: 
      errors['alias'] = 'Alias must be at least 2 charaters'
    if not EMAIL_REGEX.match(postData['email']):
      errors['email'] = 'Email is not in the correct format'
    if User.objects.filter(email=postData['email']):
      errors['email'] = 'Email is already in used'
    if len(postData['pw']) < 8:
      errors['pw'] = 'Password must be at least 8 characters'
    if postData['confirm'] != postData['pw']:
      errors['confirm'] = 'Confirm password does not match password'
    if not postData['dob']:
      errors['dob'] = 'Need to have a proper Date of Birth' 
    else:
      if datetime.strptime(postData['dob'],'%Y-%m-%d') > today:
        errors['dob'] = 'Bate of Birth cannot be in the future'

    return errors

class User(models.Model):
  name = models.CharField(max_length=45)
  alias = models.CharField(max_length=45)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  dob = models.DateTimeField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()

  def __repr__(self):
    return f'{self.first_name} {self.last_name}'

class QuoteManager(models.Manager):
  def quote_validator(self, postData):
    errors = {}
    if len(postData['quote']) < 3:
      errors['quote'] = 'Quote must be at least 3 characters'
    if len(postData['message']) < 10:
      errors['message'] = 'Message must be at least 10 characters'
    
    return errors
    
class Quote(models.Model):
  quote = models.CharField(max_length=255)
  message = models.TextField()
  creator = models.ForeignKey(User, related_name="creates")
  fav = models.ManyToManyField(User, related_name='favs')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = QuoteManager()

  def __repr__(self):
    return f'{self.quote}'