import datetime


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404 ,render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


from .models import Choice, Poll
from .forms import PollForm, EditPollForm, ChoiceForm


# Create your views here.
@login_required
def polls_list(request):
    
    polls = Poll.objects.all()
    context = {'polls': polls}
    return render(request, 'polls/polls_list.html', context)

@login_required
def add_poll(request):

    if request.method ==  "POST":
        form = PollForm(request.POST)
        if form.is_valid():
            new_poll = form.save(commit=False)
            new_poll.pub_date = datetime.datetime.now()
            new_poll.autor = request.user
            new_poll.save()
            new_choice1 = Choice(
                                poll = new_poll,
                                opcao_escolha = form.cleaned_data['choice1']
                            ).save()
            new_choice2 = Choice(
                                poll = new_poll,
                                opcao_escolha = form.cleaned_data['choice2']
                            ).save()
        messages.success(request,'Votação e opções adicionados!', extra_tags="alert alert-success")
        return redirect('polls:list')
    else:
        form = PollForm()

    context = {'form': form}
    return render(request, 'polls/add_poll.html', context)

@login_required
def edit_poll(request, poll_id):

    poll = get_object_or_404(Poll, id=poll_id)
    if request.user != poll.autor:
        return redirect('/')

    if request.method == "POST":
        form = EditPollForm(request.POST,instance=poll)
        if form.is_valid():
            form.save()
            messages.success(request,'Votação editada com sucesso!', 
                            extra_tags="alert alert-success")
        return redirect('polls:list')
    else:
        form = EditPollForm(instance=poll)

    return render(request, 'polls/edit_poll.html', {'form':form, 'poll':poll})

@login_required
def add_choice(request, poll_id):

    poll = get_object_or_404(Poll, id=poll_id)
    if request.user != poll.autor:
        return redirect('/')
    if request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            new_choice = form.save(commit = False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(request,'Opção adicionada com sucesso!', 
                            extra_tags="alert alert-success")
            return redirect('polls:list')
    else:
        form = ChoiceForm()

    return render(request, 'polls/add_choice.html', {'form':form})

@login_required
def polls_detail(request, poll_id):
    

    #poll = Poll.objects.get(id = poll_id)
    poll = get_object_or_404(Poll, id = poll_id)
    context = {'poll':poll}
    return render(request, 'polls/poll_detail.html', context)

@login_required
def poll_vote(request, poll_id):

    poll = get_object_or_404(Poll, id = poll_id)
    choice_id = request.POST.get('choice', None)
    if choice_id:
        choice = Choice.objects.get(id = choice_id)
        choice.votos += 1
        choice.save()

    else:
        messages.error(request, 'No choice was found')
        return HttpResponseRedirect(reverse("polls:detail", args=(poll_id,)))
    return render(request, 'polls/poll_results.html', {'poll':poll})