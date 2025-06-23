from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Task
from reporting.models import CompletedTask
from .forms import NewTaskForm
from datetime import date
from django.shortcuts import get_object_or_404




@login_required
def index(request):
    todos = Task.objects.filter(completed=False, in_progress=False, user=request.user).order_by('-created_at')
    completed = Task.objects.filter(completed=True, user=request.user).order_by('-completed_at').filter(
        completed_at__gte=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    )
    in_progress = Task.objects.filter(in_progress=True, user=request.user)

    context = {
        "tasks_todo": todos,
        "tasks_completed": completed,
        "tasks_in_progress": in_progress,
        "task_form": NewTaskForm(),
        "today": date.today(),  # ✅ Add this line
    }
    return render(request, 'dashboard/tasks_list.html', context)


@login_required
def in_progress(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.in_progress = not task.in_progress
    task.save()
    return redirect('dashboard:index')


@login_required
def undo_progress(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.in_progress = not task.in_progress
    task.save()
    return redirect('dashboard:index')


@login_required
def completed(request, id):
    try:
        task = Task.objects.get(id=id, user=request.user)

        if not task.completed:
            # Mark as completed
            task.completed = True
            task.completed_at = timezone.now()
            task.in_progress = False
            task.save()

            CompletedTask.objects.create(
                title=task.title,
                created_at=task.created_at,
                completed_at=task.completed_at,
                user=task.user
            )
        else:
            # Undo completion and move back to in-progress
            task.completed = False
            task.completed_at = None
            task.in_progress = True
            task.save()

        return redirect('dashboard:index')

    except Task.DoesNotExist:
        return HttpResponseNotFound("Task not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return HttpResponseServerError("Something went wrong.")


@login_required
def create(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
        return redirect('dashboard:index')
    else:
        form = NewTaskForm()
    return render(request, 'dashboard/create_task.html', {'task_form': form})


@login_required
def update(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('dashboard:index')


@login_required
def delete(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.delete()
    return redirect('dashboard:index')


@login_required
def reset_all(request):
    Task.objects.filter(user=request.user).delete()
    return redirect('dashboard:index')

@login_required
def reopen_task(request, id):
    try:
        task = Task.objects.get(id=id, user=request.user)

        if task.completed:
            task.completed = False
            task.completed_at = None
            task.in_progress = True
            task.save()

        return redirect('dashboard:index')

    except Task.DoesNotExist:
        return HttpResponseNotFound("Task not found.")
    
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        form = NewTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard:index')
    else:
        form = NewTaskForm(instance=task)

    return render(request, 'dashboard/edit_task.html', {'form': form})