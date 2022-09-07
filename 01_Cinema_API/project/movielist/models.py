from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    director = models.ForeignKey(Person, related_name="movies_directed", on_delete=models.CASCADE)
    year = models.SmallIntegerField()
    actors = models.ManyToManyField(Person, related_name="movies_cast")
