from __future__ import unicode_literals
from django.db import models
import bcrypt, re
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[0-9]).{8,}$')
DATE_REGEX = re.compile(r'^(0[1-9]|1[0-2])\/(0[1-9]|[12][0-9]|3[01])\/([12][0-9]{3})$')


class UsersManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        all_users = Users.objects.all()
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Your first name must be at least 2 characters long!"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Your last name must be at least 2 characters long!"
        if len(postData['password']) < 8:
            errors['password'] = "Password length must be a minimum of 8 characters!"
        if not postData['password'] == postData['password_confirm']:
            errors['password_same'] = "Passwords need to match!"
        if not PASSWORD_REGEX.match(postData['password']):
            errors['password_character'] = "Please enter a password with 8 or more characters with at least one capitalized letter & one number"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_type'] = "Email needs to be formatted correctly"
        for user in all_users:
            if postData['email'] == user.email:
                errors['email_used'] = "this email already exists!"
        
        return errors


    def validate_login(self,postData):
        errors = {}
        user = Users.objects.filter(email = postData['email'])
        
        if len(user) == 0:
            errors['login_email'] = "that email address is not in our database!"
            return errors
        else:
            person = user[0]
            if bcrypt.checkpw(postData['password'].encode(), person.password.encode()):
                print ("password match")
            else:
                errors['login'] = "your password did not match!"
                print ("failed password")
        return errors

    def basic_validator2(self,postData):
        errors = {}
        all_trips = Trips.objects.filter(destination=postData['destination'])
        print("*"*80)
        print(all_trips)
        if len(all_trips) > 1:
            errors['destination_used'] = "This destination already exists!"
        if len(postData['destination']) < 3:
            errors['destination'] = "A destination must consist of at least 3 characters!"
        if len(postData['plan']) < 3:
            errors['plan'] = "A plan must consist of at least 3 characters!"
        if len(postData['start_date']) < 3:
            errors['start_date'] = "A start date must be provided!"
        if len(postData['end_date']) < 3:
            errors['end_date'] = "A end date must be provided!"
        if 'end_date' in errors:
            print(errors['end_date'])
            return errors
        if 'start_date' in errors:
            print(errors['start_date'])
            return errors
        starting_date = datetime.strptime(postData['start_date'], "%Y-%m-%d")
        ending_date = datetime.strptime(postData['end_date'], "%Y-%m-%d")
        if datetime.now() >= starting_date:
            errors['starting_date'] = "Time travel is not allowed! Your trip needs to start in the future!"
        if starting_date >= ending_date:
            errors['ending_date'] = "Time travel is not allowed! Your trip needs to end later than the start date!"

        # if not DATE_REGEX.match(postData['start_date']):
        #     errors['start_date'] = "A start date must be provided!"
        # if not DATE_REGEX.match(postData['end_date']):
        #     errors['end_date'] = "A end date must be provided!"
        
        return errors

    def validate_trip(self,postData):
        errors = {}
        all_trips = Trips.objects.filter(destination=postData['destination'])
        print("*"*80)
        print(all_trips)
        if len(all_trips) >= 1:
            errors['destination_used'] = "This trip destination already exists!"
        if len(postData['destination']) < 3:
            errors['destination'] = "A destination must consist of at least 3 characters!"
        if len(postData['plan']) < 3:
            errors['plan'] = "A plan must consist of at least 3 characters!"
        if len(postData['start_date']) < 3:
            errors['start_date'] = "A start date must be provided!"
        if len(postData['end_date']) < 3:
            errors['end_date'] = "A end date must be provided!"
        if 'end_date' in errors:
            print(errors['end_date'])
            return errors
        if 'start_date' in errors:
            print(errors['start_date'])
            return errors
        starting_date = datetime.strptime(postData['start_date'], "%Y-%m-%d")
        ending_date = datetime.strptime(postData['end_date'], "%Y-%m-%d")
        if datetime.now() >= starting_date:
            errors['starting_date'] = "Time travel is not allowed! Your trip needs to start in the future!"
        if starting_date >= ending_date:
            errors['ending_date'] = "Time travel is not allowed! Your trip needs to end later than the start date!"

        
        return errors


class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

class Trips(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    plan = models.TextField()
    uploaded_by = models.ForeignKey(Users, related_name = "trips_uploaded")
    trips_on = models.ManyToManyField(Users, related_name = "users_trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def dateReleased(self):
        return self.created_at.strftime('%B %d, %Y')

    def startDate (self):
        return self.start_date.strftime('%B %d, %Y')

    def endDate (self):
        return self.end_date.strftime('%B %d, %Y')