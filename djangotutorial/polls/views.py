from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from polls.models import Question, Choice, Grade, Difficulty
from django.template import loader
from django.db.models import F
from django.urls import reverse
from django.utils import timezone
# from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic, View



# def index(request):
#     # latest_choice_list = Choice.objects.order_by('id')[:4]
#     # template = loader.get_template('polls/index.html')
#     # context = {'latest_choice_list': latest_choice_list}
#     # # output = ", ".join([c.choice_text for c in latest_choice_list])
#     # return HttpResponse(template.render(context, request))

class IndexView(generic.ListView):
    model = Question
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        # Return only published questions and order them by pub_date descending
        # so the newest questions appear first (matches test expectations).
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        ).prefetch_related("choice")
    # def get_queryset(self):
    #     return Question.objects.all()
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["all choices"] = Choice.objects.select_related("question")

# def choice(request):
#     question = Question.objects.first()
#     choice_list = question.choice.all()
#     odds = [x for x in choice_list if x.id %2 != 0]
#     template = loader.get_template('polls/choice.html')
#     # return HttpResponse(template.render({'choice_list':choice_list}, request))
#     # return render(request, "polls/choice.html", ({'choice_list':choice_list}))
#     return render(request, 'polls/choice.html', ({'odds': odds}))



class ChoiceView(generic.ListView):
    model = Choice
    template_name = "polls/choice.html"   

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/details.html", ({'question' : question}))

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"
    context_object_name = "question"

    def get_query_set(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

def results(request, question_id):
    # Only show results for questions that have been published.
    question = get_object_or_404(Question, pk=question_id, pub_date__lte=timezone.now())
    return render(request, "polls/results.html", {"question": question})

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice.get(pk=request.POST["choice"])
#     except (KeyError, Choice.DoesNotExist):
#     # Redisplay the question voting form.
#         return render(request, "polls/details.html", {"question": question, "error_message": "You didn't select a choice."})
#     else:
#         selected_choice.votes = F("votes") + 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a user hits the Back button.
#         return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

class Vote(View):
    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
            return render(request, "polls/details.html", {"question": question, "error_message": "You didn't select a choice."})
        else:
            selected_choice.votes = F("votes") + 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a user hits the Back button.
            return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
        