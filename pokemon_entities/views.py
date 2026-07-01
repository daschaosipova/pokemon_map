import folium
import json

from django.utils import timezone
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    now = timezone.localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    
    active_entities = PokemonEntity.objects.filter(
        appeared_at__lte=now,       
        disappeared_at__gte=now     
    ).select_related('pokemon')

    for entity in active_entities:
        img_url = None
        if entity.pokemon.image:
            img_url = request.build_absolute_uri(entity.pokemon.image.url)
        
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            img_url
        )

    pokemons = Pokemon.objects.all()

    pokemons_on_page = []
    for pokemon in pokemons:
        img_url = None
        if pokemon.image:
            img_url = request.build_absolute_uri(pokemon.image.url)

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    now = timezone.now()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    active_entities = PokemonEntity.objects.filter(
        pokemon=pokemon,
        appeared_at__lte=now,       
        disappeared_at__gte=now     
    ).select_related('pokemon')

    for entity in active_entities:
        img_url = None
        if entity.pokemon.image:
            img_url = request.build_absolute_uri(entity.pokemon.image.url)
        
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            img_url
        )

    img_url = request.build_absolute_uri(pokemon.image.url)
    pokemon_on_page = {
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
            'description': pokemon.description
        }
    
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_on_page
    })
