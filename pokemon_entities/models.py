from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='pokemons/', null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
