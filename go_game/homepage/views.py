from django.shortcuts import render
from game.models import Games


def homepage(request):
    recent_games = Games.objects.order_by('-id')[:20]
    context = {'recent_games': recent_games}
    return render(request, 'homepage_templates/homepage.html', context)
