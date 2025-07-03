from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from django.shortcuts import render, get_object_or_404

from .models import Question, Choice

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    
    
    # template = loader.get_template("polls/index.html")
    
    # context = {"latest_question_list": latest_question_list}    
    # return HttpResponse(template.render(context, request))    
    
    # более короткий вариант с помощью shortcut render 
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)


def detail(request, question_id):

    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Такого опроса не существует")
    
    # context = {"question": question}
    # return render(request, "polls/detail.html", context)
    
    # более короткий стиль написания благодаря shortcut get_object_or_404
    question = get_object_or_404(Question, pk=question_id)
    context = {"question": question}
    return render(request, "polls/detail.html", context)



def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {"question": question}
    return render(request, "polls/result.html", context)


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    

class DetailView(generic.DeleteView):
    model = Question
    template_name = "polls/detail.html"
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
    

class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/result.html"



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        context = {
            "question": question,
            "error_message": "Вы ничего не выбрали!"
        }
        return render(request, "polls/detail.html", context)
    else:
        # selected_choice.votes = F("votes") + 1
        selected_choice.votes = selected_choice.votes + 1
        selected_choice.save()
        
        return HttpResponseRedirect(reverse("polls:result", args=(question_id, )))