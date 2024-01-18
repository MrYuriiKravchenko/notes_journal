from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
    # Домашняя страница notes_journal
    return render(request, 'notes_journal/index.html')


@login_required
def topics(request):
    # Показать все темы
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'notes_journal/topics.html', context)


@login_required
def topic(request, topic_id):
    # Выводит одну тему и все ее записи
    topic = Topic.objects.get(id=topic_id)
    # Проверка того, что тема принадлежит текущему пользователю
    check_topic_owner(topic, request.user)

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'notes_journal/topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('notes_journal:topics')

    context = {'form': form}
    return render(request, 'notes_journal/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    # Добавляет новую запись по конкретной теме
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request.user)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('notes_journal:topic', topic_id=topic_id)

    context = {'topic': topic, 'form': form}
    return render(request, 'notes_journal/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic, request.user)

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('notes_journal:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'notes_journal/edit_entry.html', context)


def check_topic_owner(topic, user):
    if topic.owner != user:
        raise Http404
