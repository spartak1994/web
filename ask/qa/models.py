from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-id')

    def popular(self):
        return self.order_by('-rating')

class Question(models.Model):
    #id = models.SlugField(unique=True, primary_key=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    rating = models.IntegerField(default = 0)
    author = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    likes = models.ManyToManyField(User, related_name='question_likes_user')
    objects = QuestionManager()

    def __unicode__(self):
        return self.title
	
    def get_url(self):
			return reverse('question', kwargs={'question_id': self.pk})
    #def get_url(self):
    #    return reverse('question_details', kwargs={'slug': self.id})


class Answer(models.Model):
    #id = models.SlugField(unique=True, primary_key=True)
    text = models.TextField()
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    question = models.ForeignKey(Question,null=False, on_delete=models.CASCADE)
    author = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return "Answer by {0} to question {1}: {2}...".format(self.author.username, self.question.id, self.text[:50])
		
	def get_url(self):
        return reverse('question', kwargs={'question_id': self.question.id})
  