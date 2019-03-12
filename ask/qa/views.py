from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from .models import Question, Answer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.http import Http404, HttpResponseRedirect

# Create your views here.
def test(request, *args, **kwargs):
    return HttpResponse('OK')

@require_GET
def index(request, *args, **kwargs):
    #return HttpResponse('Index')
    try:
        questions = Question.objects.order_by('id')
    except Question.DoesNotExist:
        raise Http404
    paginator, page = paginate(request, questions)
    paginator.baseurl = '/?page='
    return render(request, 'index-lite.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
    })

@require_GET
def popular(request, *args, **kwargs):
    # list of questions in desc order by rating
    question_list = Question.objects.order_by('-rating')
    paginator, page, limit = paginate(request, question_list)
    paginator.baseurl = '/?page='    
    context = {
        'questions': page,
        'paginator': paginator,
        'limit': limit,
    }
    return render(request, 'popular-lite.html', context)

def question(request, question_id):
    """POST and GET methods needed"""
    q = get_object_or_404(Question, id=question_id)
    a = q.answer_set.all()
    #a = Answer.objects.filter(question=question_id).order_by('-added_at')
    form = AnswerForm(initial = {'question': question_id})
    context = {'question': q, 'answers': a, 'form': form, }
    return render(request, 'question-lite.html', context)

def paginate(request, qs):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10

    if limit > 100:
        limit = 10

    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        raise Http404	
        #page = paginator.page(paginator.num_pages)

    return paginator, page