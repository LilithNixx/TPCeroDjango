#from django.template import loader
from django.shortcuts import render, get_object_or_404
from urllib import response
from django.http import HttpResponse, HttpResponseRedirect
from . models import Question, Choice
from django.db.models import F # Permite hacer operaciones directas en la base de datos (como votos + 1)
from django.urls import reverse
from django.views import generic
#from django.http import Http404


#def index(request):
    #latest_question_list = Question.objects.order_by("-pub_date")[:5]
    #template = loader.get_template("polls/index.html")
    #context = {"latest_question_list": latest_question_list}
    #return HttpResponse(template.render(context, request))

'''
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)
'''
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_objext_name = "latest_question_list"
    
    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]
        #return the last 5 published questions
    
'''
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.NoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})
'''

class DetailView(generic.DetailView):
    model = Questiontemplate_name = "polls/detail.html"
    

'''    
#muestra los resultados de una pregunta específica, incluyendo probablemente cuántos votos tiene cada opción (Choice).
def results(request, question_id):
    #Intenta obtener la instancia de Question con ID igual a question_id.
    #Si no existe, muestra automáticamente una página 404.
    #Si existe, la guarda en la variable question.
    question = get_object_or_404(Question, pk=question_id)
    #Renderiza la plantilla HTML polls/result.html.
    #Le pasa el contexto {"question": question}.
    return render(request, "polls/result.html", {"question": question})
'''

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    
    
'''
cuando usás render(request, "plantilla.html", contexto), ese tercer parámetro (contexto) es un diccionario de Python donde:
la clave ("question") es el nombre con el que vas a acceder en la plantilla.
el valor (question) es la variable de Python que contiene los datos (en este caso, una instancia del modelo Question).
'''

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "No elegiste una opción"
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))



