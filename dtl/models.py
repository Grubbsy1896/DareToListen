from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.



class Song(models.Model):
    
    # Using a unique string ID for songs as this may be something users have to type. 
    song_id = models.CharField(max_length=32, unique=True, null=False, primary_key=True)

    title = models.CharField(max_length=300) # Watch the day when this becomes too little.
    album = models.CharField(max_length = 200, blank=True) # ^
    artists = ArrayField( models.CharField(max_length=100, blank=True) )
    release_date =models.CharField(max_length=10, blank = True) # models.DateField()
    producer = models.CharField(max_length=100, blank=True)
    writer = models.CharField(max_length=100, blank=True)
    genre = models.CharField(max_length=64, blank=True)
    duration = models.IntegerField() # To be stored in seconds. 
    explicit = models.BooleanField(default=False)

    tags = ArrayField(models.CharField(max_length=64, blank=True))

    # SPOTIFY VARIABLES
    #
    #          Storing the full url can be long
    #          Also this doesn't
    #          https://open.spotify.com/track/2rZZoZBIWW7k1i8wqyRbYl?si=150117ca84524c7e

    spotify_url = models.CharField(max_length=150) 

    #          This means we used query to find it. if false, it assumes it's correct. 
    spotify_is_best_match = models.BooleanField(default=False)

    # YOUTUBE VARIABLES
    #
    #         We will use an arrayfield because youtube can have multiple urls.
    #         We will also have a 'best' url 
    youtube_url = models.CharField(max_length=150)
    youtube_url_alternates = ArrayField(models.CharField(max_length=150, blank=True))

    #          This means we used query to find it. if false, it assumes it's correct. 
    youtube_is_best_match = models.BooleanField(default=False)

    # Image Urls
    image_url = models.CharField(max_length= 300, blank=True) # Idk how long its gonna be

class Playlist(models.Model):

    playlist_id = models.CharField(max_length=32, unique=True, null=False, primary_key=True)

    title = models.CharField(max_length=150)