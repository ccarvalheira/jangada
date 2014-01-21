from django.db import models



class Choice(models.Model):
    question = models.CharField(max_length=50)
    choice_text = models.CharField(max_length=100)
    votes = models.IntegerField()



    def __unicode__(self):
        return self.choice_text




class Question(models.Model):
    question_text = models.CharField(max_length=100)
    pub_date = models.DateTimeField()



    def __unicode__(self):
        return self.question_text


