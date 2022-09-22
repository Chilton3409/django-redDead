from django.db import models
from django.urls import reverse
from django.utils import timezone
import datetime
from django.core.exceptions import ValidationError
from django.core import validators


# Create your models here.

class Character(models.Model):
    #model representing a single red dead character. 
    first_name = models.CharField(max_length=100,validators=[validators.MaxLengthValidator],help_text="Enter the characters first name")
    last_name = models.CharField(max_length=100,validators=[validators.MaxLengthValidator],help_text="Enter the characters last name")
    related_gang = models.ForeignKey('Group', null=True, on_delete=models.SET_NULL, help_text="Enter group information.")
    summary = models.TextField(max_length=1000,validators=[validators.MaxLengthValidator] ,null=True, blank=True, help_text="Enter character's biography")
    creation_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True, help_text="Enter date of birth.")

    date_of_death = models.DateField('Died', null=True, help_text="Enter date of death.")


    class Meta:
        ordering = ['first_name',]

    def get_absolut_url(self):
        return reverse("reddead:character_detail", args=[str(self.id)])

    def __str__(self):
        return self.first_name

class Group(models.Model):
    #model representing the group a character belongs to.
    title = models.CharField(max_length=200)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the group.")
    characters = models.ManyToManyField(Character,null=True, blank=True, help_text="Use command + click to select multiple characters.")
    creation_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("reddead:group_detail", args=[str(self.id)])
    
    
#models representing a question object
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date_published', auto_now_add=True)

    #string methods
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

#model representing a choice
class Choice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    #string methods
    def __str__(self):
        return self.choice_text

