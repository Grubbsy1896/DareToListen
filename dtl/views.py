from django.shortcuts import render
from django.http import HttpResponse
from .forms import CreateSongForm
from .spotilib import spotify_request_song, strip_url, clean_title
from .ylib import get_yt_urls
from .models import Song
from ratelimit.decorators import ratelimit
# Create your views here.


def index(request):
    return HttpResponse("You've accessed the index of IDYTL Congrats. ")


@ratelimit(key='ip', rate='20/m', method='POST')
def create_song(request):
    
    was_limited = getattr(request, 'limited', False)

    request.create_song_fail     = False
    request.create_song_fail_msg = "IDK what happened..."
    request.create_song_suck = False
    error = False
    request.create_song_suck = True

    if request.method == 'POST': 

        form = CreateSongForm(request.POST)
        if form.is_valid():

            url = form.cleaned_data['song_url']
            try:
                spid = strip_url(url)
            except:
                request.create_song_fail     = True
                request.create_song_fail_msg = "Invalid spotify url"
                error = True
                spid = ""


            # We need to check here now actually.
            # ANTI - SPAM CHECK
            url = f"https://open.spotify.com/track/{spid}"
            sim_songs = Song.objects.filter(spotify_url=url).exists()
            if sim_songs:
                request.create_song_fail = True
                request.create_song_fail_msg = "That Song Already Exists"
          
            elif error:
                pass # Already listed the data needed here.
        
            elif was_limited:
                request.create_song_fail = True
                request.create_song_fail_msg = "Stop adding songs so quickly!"

            else:
                try:
                    
                    data = spotify_request_song(spid)
                    
                except:
                    data = {}
                    request.create_song_fail = True
                    request.creeate_song_fail_msg = "Spotify Url Not Valid"
                    error = True


                try:
                    
                    song_id = clean_title(data['title'])

                    #idcheck = Song.objects.filter(song_id=song_id).exists()

                    if len(song_id) > 29:
                        song_id = song_id[0:29]

                    inte = 1
                    while True: # Will cast inte to None when I'm done.
                        idcheck = Song.objects.filter(song_id=song_id).exists()
                        if idcheck:
                            newid = f"{song_id}({inte})"
                            if Song.objects.filter(song_id=newid).exists():
                                inte+=1 
                            else:
                                song_id = newid
                                break
                        else:
                            add_song = True
                            break
                except:
                    
                    request.create_song_fail     = True
                    error = True
                    request.create_song_fail_msg = "Not a real spotify song!"
                


                if not error:
                    try:
                        new_song = Song.objects.create(song_id=song_id, title=data['title'], 
                                                    album = data['album'],
                                                    artists = data['artists'],
                                                    release_date =  data['release_date'],
                                                    duration = data['duration'],
                                                    explicit = data['explicit'],
                                                    image_url = data['image_url'],
                                                    spotify_url = data['external_url'], 
                                                    tags = [],
                                                    youtube_url_alternates = [],
                                                    )
                        new_song.save()
                        request.create_song_suck = True
                    except Exception as e:
                        print("Unexpected error: ", e)
                        request.create_song_fail = True
                        request.create_song_fail_msg = "An Unexpected Error Occured."
                        
            # This is the end of an if statement determining things.

    else: 
        form = CreateSongForm()


    return render(request, 'createsong.html', {'form': form})


# Api GET func
def song(request, sid=None):
    song_list = list(Song.objects.all())
    p = request.session.get('page', 0)

    if request.method == 'POST':

        try:

            if 'next' in request.POST:
                mode = "Next"
            else:
                mode = "Prev"
        except Exception as e:
            print(e)
            mode = "None"

        
        if mode == "Next":
            p += 1
        elif mode == 'Prev':
            p -= 1
        else:
            p = p

        if p >= len(song_list):
            p = 0
        elif abs(p) >= len(song_list):
            p = 0

        request.session['page'] = p
    
    song = song_list[p]

    if sid is not None:
        try:
            song = Song.objects.get(pk=sid)
        except:
            pass
   

    if song.youtube_url == "":
        get_yt_urls(song)
    

    request.p = p
    return render(request, 'song.html', {'song': song})
    




