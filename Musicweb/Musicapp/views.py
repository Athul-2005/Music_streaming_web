from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q, Max, Min
from .models import Songs, playlist
from django.contrib import messages


@login_required
def home(request):
    # Query the database for all songs
    songs = Songs.objects.all()
    # Query the database for playlists that belong to the logged-in user
    playlists = playlist.objects.filter(user=request.user)
    # Pass the list of songs and playlists to the template
    context = {
        'Songs': songs,
        'playlists': playlists
    }
    return render(request, 'home.html', context)

def login_view(request):
    if request.method == 'POST':
        if 'username' in request.POST:
            uname = request.POST['username']
            passwor = request.POST['password']
            user = authenticate(request, username=uname, password=passwor)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'Auth/login.html', {'msg': 'Invalid User'})
        elif 'suname' in request.POST:
            username = request.POST['suname']
            email = request.POST['semail']
            password = request.POST['spass']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect('home')
    return render(request, 'Auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@user_passes_test(lambda u: u.is_superuser, login_url='/')
def add_song(request):
    songs = Songs.objects.all()
    if request.method == 'POST':
        sname = request.POST['sname']
        mimage = request.FILES['mimage']
        sgenre = request.POST['sgenre']
        artist = request.POST['artist']
        audio = request.FILES['audio']
        
        # Find the smallest available ID
        used_ids = set(Songs.objects.values_list('id', flat=True))
        new_id = 1
        while new_id in used_ids:
            new_id += 1
            
        # Create song with the specific ID
        song = Songs.objects.create(
            id=new_id,
            sname=sname, 
            mimage=mimage, 
            sgenre=sgenre, 
            Artist=artist, 
            audio=audio
        )
        return redirect('home')
    return render(request, 'songadd.html', {'Songs': songs})

@user_passes_test(lambda u: u.is_superuser, login_url='/')
def delete_song_by_name(request):
    if request.method == 'POST':
        song_name = request.POST.get('song_name')
        try:
            song = get_object_or_404(Songs, sname=song_name)
            song.delete()
            return redirect('add_song')
        except Exception as e:
            messages.error(request, f"Error deleting song: {str(e)}")
            return redirect('add_song')
    return render(request, 'delete_song.html')

def playsong(request, song_id):
    # Get all songs to determine boundaries
    all_songs = Songs.objects.all()
    max_id = all_songs.aggregate(Max('id'))['id__max']
    min_id = all_songs.aggregate(Min('id'))['id__min']
    
    # Ensure song_id is within bounds
    if song_id < min_id:
        song_id = min_id
    elif song_id > max_id:
        song_id = max_id
        
    song = get_object_or_404(Songs, id=song_id)
    song.play()  # Increment play count
    
    # Get previous and next song IDs with bounds checking
    prev_id = song_id - 1 if song_id > min_id else song_id
    next_id = song_id + 1 if song_id < max_id else song_id
    
    # Only show playlists that belong to the current user
    playlists = playlist.objects.filter(user=request.user) if request.user.is_authenticated else []
    
    context = {
        'song': song,
        'playlists': playlists,
        'prev_id': prev_id,
        'next_id': next_id
    }
    return render(request, 'playsong.html', context)

def search_view(request):
    query = request.GET.get('search', '').strip()  # Ensure query is stripped of extra spaces
    results = Songs.objects.filter(
        Q(sname__icontains=query) | Q(Artist__icontains=query) | Q(sgenre__icontains=query)
    ) if query else []  # Ensure case sensitivity for 'Artist' field is handled
    context = {
        'query': query,
        'results': results
    }
    return render(request, 'search.html', context)

@login_required
def playlist_detail(request, playlist_id):
    # Use get_object_or_404 with a filter for the current user
    playlist_obj = get_object_or_404(playlist, id=playlist_id, user=request.user)
    context = {
        'playlist': playlist_obj,
        'songs': playlist_obj.songs.all()
    }
    return render(request, 'playlist.html', context)

@login_required
def add_to_playlist(request, song_id):
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist')  
        # Ensure the playlist belongs to the current user
        playlist_obj = get_object_or_404(playlist, id=playlist_id, user=request.user)
        song = get_object_or_404(Songs, id=song_id)
        playlist_obj.songs.add(song)
        playlist_obj.save()  # Ensure changes are saved
        messages.success(request, f"{song.sname} has been added to {playlist_obj.pname}.")
        return redirect('playsong', song_id=song_id)

@login_required
def create_playlist(request):
    if request.method == 'POST':
        playlist_name = request.POST.get('playlist_name')

        if playlist_name:
            # Ensure the playlist is associated with the logged-in user
            new_playlist, created = playlist.objects.get_or_create(pname=playlist_name, user=request.user)
            if created:
                messages.success(request, f"Playlist '{playlist_name}' has been created.")
            else:
                messages.warning(request, f"Playlist '{playlist_name}' already exists.")
            return redirect('playlist', playlist_id=new_playlist.id)
        else:
            messages.error(request, "Playlist name cannot be empty.")

    return render(request, 'create_playlist.html')

@login_required
def rename_playlist(request, playlist_id):
    Playl = get_object_or_404(playlist, id=playlist_id, user=request.user)

    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        if new_name:
            Playl.pname = new_name
            Playl.save()
            messages.success(request, f"Playlist renamed to '{new_name}'.")
        
    return redirect('playlist', playlist_id=Playl.id)

@login_required
def delete_playlist(request, playlist_id):
    playlist_obj = get_object_or_404(playlist, id=playlist_id, user=request.user)

    if request.method == 'POST':
        playlist_name = playlist_obj.pname
        playlist_obj.delete()
        messages.success(request, f"Playlist '{playlist_name}' has been deleted.")
        
    return redirect('home')

@login_required
def remove_from_playlist(request, playlist_id, song_id):
    playl = get_object_or_404(playlist, id=playlist_id, user=request.user)
    song = get_object_or_404(Songs, id=song_id)

    if request.method == 'POST':
        playl.songs.remove(song)
        messages.success(request, f"'{song.sname}' has been removed from '{playl.pname}'.")
        
    return redirect('playlist', playlist_id=playl.id)