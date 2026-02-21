from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Games, Positions


class CreateGameForm(forms.Form):
    board_size = forms.ChoiceField(choices=Games.BoardSize.choices)
    color = forms.ChoiceField(choices=Games.Player.choices)


def create_new_game(request):
    if request.method == 'POST':
        form = CreateGameForm(request.POST)
        if form.is_valid():
            game = Games.objects.create(
                board_size=int(form.cleaned_data['board_size']),
                current_player=form.cleaned_data['color'],
            )
            first_position = Positions.objects.create(
                game=game,
                previous=None,
                board={},
            )
            game.current_position = first_position
            game.title = f'Игра #{game.id}'
            game.save(update_fields=['current_position', 'title'])
            return redirect('homepage:homepage')
    else:
        form = CreateGameForm()

    return render(request, 'game_templates/create_new.html', {'form': form})


def load_game(request, pk):
    return HttpResponse(f'Страница игры {pk} пока не реализована')
