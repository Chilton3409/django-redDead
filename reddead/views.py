from django.shortcuts import render
from .models import Character, Group, Question, Choice
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone 
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django import forms

from django.urls import reverse




# Create your views here.
def index(request):
    num_characters = Character.objects.all().count()
    num_groups = Group.objects.all().count()

    # Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    #last 5 characters created
    last_five_dead = Character.objects.filter(date_of_death__lte=timezone.now()).order_by('date_of_death')[:5]


    #number of visits to this view, as counted in the session variable
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1


    context = {
        'num_characters': num_characters,
        'num_visits': num_visits,
        'num_groups': num_groups,
        'last_five_dead': last_five_dead,





    }
    return render(request, 'reddead/index.html', context=context)

class CharacterListView(generic.ListView):
    paginate_by =  10
    model = Character
    template_name = 'reddead/characters.html'
    context_object_name = 'character_list'
   

class CharacterDetailView(generic.DetailView):
    model = Character
    template_name = 'reddead/character_detail.html'
    context_object_name = 'character' 

#views for generic create, edit, update, and delete
class CharacterCreate(CreateView):
    model = Character
    fields = ['first_name', 'last_name','summary','related_gang', 'date_of_birth', 'date_of_death']
    template_name = 'reddead/character_create.html'
    initial = {'date_of_death': '11/06/1790'}
    success_url = reverse_lazy('reddead:characters')

    


class CharacterUpdate(UpdateView):
    model = Character
    template_name = 'reddead/character_update.html'
    fields = ['first_name', 'last_name','summary','related_gang', 'date_of_birth', 'date_of_death']
    success_url = reverse_lazy('reddead:characters')

class CharacterDelete(DeleteView):
    model = Character
    success_url = reverse_lazy('reddead:characters')

#views for group list and detail

class GroupListView(generic.ListView):
    paginate_by: 5
    model = Group
    template_name = 'reddead/groups.html'
    context_object_name = 'group_list'
    

class GroupDetailView(generic.DetailView):
    model = Group
    template_name = 'reddead/group_detail.html'
    context_object_name = 'group'

class GroupCreateView(generic.CreateView):
    model = Group
    template_name = 'reddead/group_create.html'
    fields = ['title', 'summary', 'characters']
    success_url = reverse_lazy('reddead:groups')

class GroupUpdateView(generic.UpdateView):
    model = Group
    template_name = 'reddead/group_update.html'
    fields = ['title', 'summary', 'characters']
    success_url = reverse_lazy('reddead:groups')


class GroupDeleteView(generic.DeleteView):
    model = Group
    success_url = reverse_lazy('reddead:groups')
    


#views for wildlife index, detail and vote
class WildlifeIndexView(generic.ListView):
    template_name = 'reddead/wildlife.html'
    context_object_name = 'latest_question_list'
    paginate_by: 5

    def get_queryset(self):
        # Return the last 5 published questions
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

#wildlife question detail view
class WildlifeDetailView(generic.DetailView):
    model = Question
    template_name = 'reddead/wildlife_detail.html'

# wildlife vote results view
class WildLifeResultsView(generic.DetailView):
    model = Question
    template_name = 'reddead/wildlife_results.html'
    
    
    
# vote function
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #redisplay voting form
        return render(request, 'reddead/wildlife_detail.html', {'question': question,
                                                            'error_message': "You didn't select a choice..",})

    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('reddead:results', args=(question_id,)))

