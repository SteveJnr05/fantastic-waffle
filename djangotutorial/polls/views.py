from django.shortcuts import render
from django.http import HttpResponse
from polls.models import Question, Choice, Grade, Difficulty
from django.template import loader


def index(request):
    latest_choice_list = Choice.objects.order_by('id')[:4]
    template = loader.get_template('polls/index.html')
    context = {'latest_choice_list': latest_choice_list}
    # output = ", ".join([c.choice_text for c in latest_choice_list])
    return HttpResponse(template.render(context, request))

def detail(request):
    question = Question.objects.first()
    choice_list = question.choice.all()
    template = loader.get_template('polls/choice.html')
    # return HttpResponse(template.render({'choice_list':choice_list}, request))
    return render(request, "polls/choice.html", ({'choice_list':choice_list}))

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

