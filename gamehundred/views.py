from django.shortcuts import render
from .models import Game

# Create your views here.

def index(request):
    """View function for home page of site."""
    num_games = Game.objects.count()
    game_list = Game.objects.all()

    context = {
        'num_games': num_games,
        'game_list': game_list,
    }
    print(game_list)
    return render(request, 'index.html', context=context)

from django.views import generic
from django.http import HttpResponse
from gamehundred.game_of_hundred import game_of_one_hundred as goh

#July 30
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from gamehundred.game_of_hundred_django import session_restart
from gamehundred.forms import ChooseMoveStart
def game_detail(request, pk):
    game = Game.objects.all()[pk-1]
    context = {
        'game': game,
    }
    [moves, moveholders, numbers_before, numbers_after, number_cur] = session_restart(['moves', 'moveholders', 'numbers_before', 'numbers_after'], ['number_cur'], request)#defines empty coockies defining them if absent

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ChooseMoveStart(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            who_moves_first = form.cleaned_data['move_first']
            if who_moves_first == '2':#first computer move
                goh_cur = goh(goal=game.goal, number_max_avail=game.max_avail, number_cur=0)
                move = goh_cur.comp_move()
                request.session['number_cur'] = move
                request.session['moves'] = [move]
                request.session['moveholders'] = ['computer']
                request.session['numbers_before'] = [0]
                request.session['numbers_after'] = [move]
            else:
                request.session['number_cur'] = 0
                request.session['moves'] = []
                request.session['moveholders'] = []
                request.session['numbers_before'] = []
                request.session['numbers_after'] = []

            # redirect to a new URL:
            return HttpResponseRedirect('{:d}/play'.format(pk))
    else:
        form = ChooseMoveStart(initial={'move_first': '1'})
        context['form'] = form
    
    return render(request, 'gamehundred/game_detail.html', context=context)

from gamehundred.forms import HumanMoveForm
#----
def game_goh_play(request, pk):

    is_oversum = 0
    game = Game.objects.all()[pk-1]
    moves = request.session.get('moves', [])
    moveholders = request.session.get('moveholders', [])
    numbers_before = request.session.get('numbers_before', [])
    numbers_after = request.session.get('numbers_after', [])
    number_cur = request.session.get('number_cur', 0)
    is_end_of_game = request.session.get('is_end_of_game', 0)

    context = {
                'number_min_avail': game.number_init+1,
                'is_out_of_range': False,
            }

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = HumanMoveForm(request.POST)
        if (form.is_valid() and form.cleaned_data and form.cleaned_data['restart'] == True) or (form.is_valid() and is_end_of_game): #restart
            tmp = session_restart(['moves', 'moveholders', 'numbers_before', 'numbers_after'], ['number_cur', 'is_end_of_game'], request)#defines empty coockies defining them if absent
            return HttpResponseRedirect('../{:d}'.format(pk))
        elif form.is_valid() and form.cleaned_data and (form.cleaned_data['move_cur'] <= game.number_init or form.cleaned_data['move_cur'] > game.max_avail):#keep the user with the same page and show the out of range error message
            context['is_out_of_range'] = True
            move = form.cleaned_data['move_cur']
        elif form.is_valid():
            # process the data in form.cleaned_data as human move 
            move = form.cleaned_data['move_cur']
            numbers_before.append(number_cur)
            number_cur += move
            moves.append(move)
            moveholders.append('human')
            numbers_after.append(number_cur)
            if number_cur >= game.goal:
                is_end_of_game = 1
            if number_cur > game.goal:
                is_oversum = 1
            # ---- end of human move
            # computer move
            if not is_end_of_game:
                numbers_before.append(number_cur)
                goh_cur = goh(goal=game.goal, number_max_avail=game.max_avail, number_cur=number_cur)
                move = goh_cur.comp_move()
                moves.append(move)
                moveholders.append('computer')
                numbers_after.append(goh_cur.number_cur)
                number_cur = goh_cur.number_cur
                if number_cur == game.goal:
                    is_end_of_game = 1
            #----End of computer move

            #Save cookies
            request.session['number_cur'] = number_cur
            request.session['moves'] = moves
            request.session['moveholders'] = moveholders
            request.session['numbers_before'] = numbers_before
            request.session['numbers_after'] = numbers_after
            context['move'] = move
    # If this is a GET (or any other method) do nothing
    else:
        pass

    form = HumanMoveForm(initial={'move_cur': '', 'restart': False})
    context['form'] = form
    if len(moves) > 0:
        context['comp_move_last'] = moves[-1]
    context['number_cur'] = request.session['number_cur']
    context['history'] = zip(request.session['numbers_before'], request.session['moves'], request.session['moveholders'], request.session['numbers_after'])
    context['game'] = Game.objects.all()[pk-1]
    context['is_end_of_game'] = is_end_of_game
    context['is_oversum'] = is_oversum
    if len(moveholders) > 0:
        context['moveholder_last'] = moveholders[-1]
    else:
        context['moveholder_last'] = ''
    return render(request, 'gamehundred/game_goh_play.html', context=context)



