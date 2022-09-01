from xmlrpc.client import DateTime
from django.db import models
# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    slug = models.CharField(max_length=10, unique=True,
                            default="question")

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Entrenamientos(models.Model):
    Fecha=models.DateTimeField()
    Grado1=models.TextField(null=True)
    Instructor=models.TextField(null=True)
    Grado2=models.TextField(null=True)
    Piloto=models.TextField(null=True)
    Grado3=models.TextField(null=True)
    CoPiloto=models.TextField(null=True)
    Grado4=models.TextField(null=True)
    Observador=models.TextField(null=True)
    Hora_Entrada=models.TimeField(auto_now=False, auto_now_add=False)
    Hora_Salida=models.TimeField(auto_now=False, auto_now_add=False)
    Horas=models.FloatField(null=True)
    Calificacion=models.IntegerField(null=True)
    IFR=models.FloatField(null=True)
    NVR=models.FloatField(null=True)
    Observaciones=models.TextField(null=True)
    Tipoentrenamiento=models.TextField(null=True)
    Fuerza=models.TextField(null=True)
    Tipo=models.TextField(null=True)
    Unidad=models.TextField(null=True)

    def __str__(self):
        return self.Fuerza