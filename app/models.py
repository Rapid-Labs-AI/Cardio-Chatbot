from django.db import models

class Chat_answers(models.Model):
    Answer = models.CharField(max_length=10000)

    def __str__(self):
        model_name = self.__class__.__name__
        fields_str = ", ".join((f"{field.name}={getattr(self, field.name)}" for field in self._meta.fields))
        return f"{model_name}({fields_str})"

# Create your models here.
    
