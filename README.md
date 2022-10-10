# DareToListen
Django Site to allow sharing and translation of spotify and youtube playlists.


Only the app will be shared. This app uses many pip libraries.
It is not complete. 


Requirements:
- spotipy
- pytube
- django-bootstrap-v5
- django-crispy-forms
- django-ratelimit
- djangorestframework
- django-cors-headers


Current "Vulnerabilitites" (Errors)
- Getting 10 songs that have a title longer than 29 characters will cause a db error. 
- You can force a video into the assumed best match slot by changing very few things about your channel. (it will have to show up in the top results as well)
