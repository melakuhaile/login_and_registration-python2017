from __future__ import unicode_literals

from django.db import models
import re
import bcrypt


NUM_REGEX = re.compile('[0-9]')
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")



def uni_str_dict(mydict):
    data = {}
    for key, val in mydict.iteritems():
        if key != 'csrfmiddlewaretoken':
         data[key] = str(val)
    return data

# Create your models here.
class UserManager(models.Manager):
    def makeUser(self,form):
        flag = False
        errors = {}
        data = uni_str_dict(form)

        for val in data.itervalues():
            if len(val) < 1:
                flag = True
                errors['blank'] = 'All fields are required , please fill in the required attributes'
            
                break

        if len(data['password']) < 8:
            errors['password'] = 'password must be longer than 8 characters' 
            flag = True
        if data['password'] != data['confirm_pw']:
            errors['password'] = 'password must match passowrd confirm' 
            flag = True
         
            
        if len(data['first_name']) < 3:
            errors['first_name'] = 'first_Name must be longer than three characters' 
            flag = True
        if len(data['last_name']) < 3:
            errors['last_name'] = 'last_name must be longer than three characters' 
            flag = True

        if not EMAIL_REGEX.match(data['email']):
            flag = True
            errors['email'] = 'email not valid'

        for Char in range(len(data['first_name'])):
            if NUM_REGEX.match(data['first_name'][Char]):
                errors['first_name_number'] = 'no numbers are allowed in first names.'
                flag = True
                break

        for Char in range(len(data['last_name'])):

            if NUM_REGEX.match(data['last_name'][Char]):
                errors['last_name_number'] = 'no numbers are allowed in last names.'
                flag = True
                break

        if flag ==True:
            return(False, errors)

        user = User.manager.create(first_name=data['first_name'],last_name=data['last_name'], email=data['email'], password=bcrypt.hashpw(data['password'],bcrypt.gensalt()))
        # self === User.manager
        return (True, user)
    def UserLogin(self,form):
        flag = False
        errors = {}
        data = uni_str_dict(form)
        try:
            current_user = User.manager.get(email=data['email'])
        except Exception:
            errors['email'] = 'that email does not appear in our records'
            return(False, errors)
            
        
        if not bcrypt.hashpw(data['password'].encode(),current_user.password.encode()):
            flag = True
            errors['passowrd'] = 'that password doesnt match the onw we have in record'
        if flag:
            return(False, errors)
        return(True, current_user)


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at =models.DateTimeField(auto_now = True)
    manager = UserManager()