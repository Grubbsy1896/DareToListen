from pytube import Search
from pytube import Playlist
from .models import Song


def get_best_match(objs, song):

    good_strings = [
        "Official Music Video",
        "Lyrics",
        "Official Audio"
    ]

    # Parse through objs.

    scores = {}

    ide = 0
    for o in objs:
        score = 0
        ide += 1

        if (str(song.title).lower() in str(o.title).lower())   or (str(song.title).lower() == str(o.title).lower()):
            score += 2
        if (str(song.artists[0]).lower() in str(o.author).lower()) or (str(song.artists[0]).lower() == str(o.author).lower()):
            score += 3 # Higher priority because it's a song by this artist...

        for s in good_strings:
            if s.lower() in str(o.title).lower():
                score += 1

        
        if score >= 1:
            scores[str(ide)] = {'o': o, 'score': score}
    
    # for s in scores:
    #     print(s, "  ", scores[s]['o'].title, scores[s]['score'])

    hi = 0
    he = ""
    for s in scores:

        score = scores[s]['score']
        if score >= hi:
            hi = score
            he = s

    top_scorers = []
    for s in scores:
        if scores[s]['score'] >= hi-1:
            top_scorers.append(scores[s])


    return top_scorers

def get_yt_urls(song):

    search_string = f"{song.title} {song.artists[0]}"

    search = Search(search_string)

    best_results = get_best_match(search.results, song)

    top_song = None

    for r in  best_results:
        if top_song is None:
            top_song = r
        
        if r['score'] >= top_song['score']:
            top_song = r
    
    best_results.remove(top_song)

    new_list = []
    for songg in best_results:
        new_list.append(songg['o'].watch_url)

    print(top_song['o'])
    song.youtube_url = top_song['o'].watch_url
    song.youtube_url_alternates = new_list
    song.youtube_is_best_match = True
    song.save()

