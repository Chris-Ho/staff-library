from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser, PermissionsMixin


# Create your models here.
class Book(models.Model):
    bookID = models.AutoField(primary_key=True)
    imageUrl = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    description = models.TextField()
    quantity = models.IntegerField()

    def getID(self):
        return self.bookID
    def getTitle(self):
        return self.title
    def getDesc(self):
        return self.description
    def getImage(self):
        return self.imageUrl
    def getCount(self):
        return self.quantity


#Extend default auth class to replace username with email  // sources online
class UserManager(BaseUserManager):
    use_in_migrations = True
    #override
    def _create_user(self, email, firstname, lastname, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, firstname=firstname, lastname=lastname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, firstname, lastname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, firstname, lastname, password, **extra_fields)

    def create_superuser(self, email, firstname, lastname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, firstname, lastname, password, **extra_fields)

#Represents users
class User(AbstractUser):
    username = None
    email = models.EmailField(('email address'), unique=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    objects = UserManager()

    

#Represents loans currently taken out (loans table)
class Loan(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    bookID = models.ForeignKey(Book, on_delete=models.CASCADE)
    returnDate = models.DateField()

    def getUserID(self):
        return self.userID
    def getBookID(self):
        return self.bookID

    def getReturnDate(self):
        return self.returnDate

'''
Book: image, title, desc
User: name, lastname, email
Loans: User, BookID, return date
'''

