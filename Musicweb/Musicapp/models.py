from django.db import models
from django.contrib.auth.models import User


class Songs(models.Model):
    sname = models.CharField(max_length=50)
    mimage = models.ImageField(upload_to='media/images/', default='media/images/default.jpg')
    sgenre = models.CharField(max_length=50)
    Artist = models.CharField(max_length=50)
    audio = models.FileField(upload_to='audiofiles', default='Media/audiofiles/default.mp3')
    playedbefore = models.BooleanField(default=False)
    play_count = models.IntegerField(default=0)

    def __str__(self):
        return self.sname

    def play(self):
        self.play_count += 1
        self.save()
        if self.play_count > 2:
            popular_song, created = popularsongs.objects.get_or_create(sname=self)
            popular_song.popularity_score = self.play_count
            popular_song.save()

def get_default_user():
    # Get or create a default user
    user, created = User.objects.get_or_create(username='default_user')
    return user.id

class playlist(models.Model):  
    pname = models.CharField(max_length=100)
    songs = models.ManyToManyField(Songs)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)

    def __str__(self):
        return self.pname

class popularsongs(models.Model):
    sname = models.ForeignKey(Songs, on_delete=models.CASCADE)
    popularity_score = models.IntegerField(default=0)
    added_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.sname} with score {self.popularity_score}"


