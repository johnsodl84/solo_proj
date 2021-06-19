from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.


def index(request):
    return render(request, "games/index.html")


def register(request):
    errors = User.objects.register_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=bcrypt.hashpw(
                request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/games')


def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/games')


def game_all(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            'all_games': Game.objects.all(),
            'this_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'games/game_all.html', context)


def create_game(request):
    errors = Game.objects.game_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/games')
    else:
        user = User.objects.get(id=request.session["user_id"])
        game = Game.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            creator=user
        )
        user.favorited_games.add(game)

        return redirect(f'/games/{game.id}')

def show_one(request, game_id):
    context = {
        'game': Game.objects.get(id=game_id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "games/show_one.html", context)


def update(request, game_id):
    game = Game.objects.get(id=game_id)
    game.description = request.POST['description']
    game.save()

    return redirect(f"/games/{game_id}")


def delete(request, game_id):
    game = Game.objects.get(id=game_id)
    game.delete()

    return redirect('/games')


def favorite(request, game_id):
    user = User.objects.get(id=request.session["user_id"])
    game = Game.objects.get(id=game_id)
    user.favorited_games.add(game)

    return redirect(f'/games/{game_id}')


def unfavorite(request, game_id):
    user = User.objects.get(id=request.session["user_id"])
    game = Game.objects.get(id=game_id)
    user.favorited_games.remove(game)

    return redirect(f'/games/{game_id}')


def logout(request):
    request.session.flush()

    return redirect('/')
