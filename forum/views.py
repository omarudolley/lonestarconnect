from django.shortcuts import render, get_object_or_404, redirect
from .models import Forum, Thread, Post
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from .forms import NewTopicForm, TopicReply, UpdateForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q


def home(request):
    query = ''
    if request.GET:
        query = request.GET.get('q', ' ')

    threads = get_query(query)

    boards = Forum.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(threads, 20)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        topics = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        topics = paginator.page(paginator.num_pages)
    return render(request,'forum/index.html', {'boards':boards,'topic':topics, 'query':query})

# def topic(request,pk):
#     try:
#         board = Forum.objects.get(pk=pk)
#     except Forum.DoesNotExist:
#         raise Http404
#     return render(request,'forum/thread.html', {'board':board})
def topic(request,pk):
    board = get_object_or_404(Forum,pk=pk)
    queryset= board.thread.order_by('-last_updated').annotate(replies=Count('post')-1)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 20)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        topics = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        topics = paginator.page(paginator.num_pages)
    return render(request,'forum/topics.html',{'board':board,'topic':topics})

def about(request):
    return render(request, 'forum/about.html')

@login_required
def new_topic(request, pk ):
    board = get_object_or_404(Forum,pk=pk)

    if request.method == 'POST':
        form = NewTopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.forum =board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                image= form.cleaned_data.get('image'),
                thread = topic,
                created_by = request.user
            )
            return redirect('forum-topic',pk=board.pk)
    else:
        form = NewTopicForm()
    return render(request,'forum/new_topic.html',{'board':board, 'form':form})


def topics_post(request, pk , thread_pk):
    topic = get_object_or_404(Thread,forum__pk=pk,pk=thread_pk)
    topic.views +=1
    topic.save()
    return render(request,'forum/thread_posts.html',{'topic':topic})


@login_required
def reply_post(request,pk,thread_pk):
    topic = get_object_or_404(Thread,forum__pk = pk, pk = thread_pk)
    if request.method == 'POST':
        form = TopicReply(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit= False)
            post.thread = topic
            post.created_by = request.user
            post.save()
            return redirect('thread_post',pk = topic.forum.pk ,thread_pk =topic.pk)
    else:
        form = TopicReply()
    return render(request,'forum/new_post.html', {'topic':topic,'form':form})


@login_required
def edit_post(request,pk,thread_pk,post_pk):
    post = get_object_or_404(Post,thread__forum__pk =pk , thread__pk = thread_pk, pk = post_pk)
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=post)
        if form.is_valid():
            post= form.save()
            return redirect('thread_post',pk=post.thread.forum.pk, thread_pk= post.thread.pk)
    else:
        form=UpdateForm(instance=post)
        return render(request,'forum/update_post.html',{'form':form,'post':post})
@login_required
def delete_post(request,pk,thread_pk,post_pk):
    post = get_object_or_404(Post,thread__forum__pk=pk, thread__pk = thread_pk, pk = post_pk)
    if request.method == 'POST':
        post.delete()
        return redirect('thread_post',pk=post.thread.forum.pk, thread_pk= post.thread.pk)
    else:
        return render(request, 'forum/post_confirm_delete.html',{'post':post})



def get_query(query=None,board=None):
    queryset=[]
    queries=query.split(' ')
    for q in queries:
        topics = Thread.objects.filter(
        Q(title__icontains=q)
        ).distinct().order_by('-last_updated')
        for topic in topics:
            queryset.append(topic)
    return list(set(queryset))
