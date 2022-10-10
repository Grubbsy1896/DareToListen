from django import forms



class CreateSongForm(forms.Form):
    song_url = forms.CharField(label="Spotify Song Link", help_text="right click, share, copy song link", required = True)
    yt_url = forms.CharField(label="YT Link", help_text="Not an implemented Feature currently...", required = False)