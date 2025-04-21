from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import UserRegisterForm, TodoItemForm
from .models import TodoItem

def register(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('todo_list')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def todo_list(request):
    """Display the list of todo items and handle adding new items."""
    todos = TodoItem.objects.filter(user=request.user).order_by('-created_at')
    form = TodoItemForm()
    
    if request.method == 'POST':
        form = TodoItemForm(request.POST, request.FILES)
        if form.is_valid():
            todo_item = form.save(commit=False)
            todo_item.user = request.user
            todo_item.save()
            messages.success(request, 'Task added successfully!')
            return redirect('todo_list')
    
    context = {
        'todos': todos,
        'form': form,
    }
    return render(request, 'todo_list.html', context)

@login_required
def edit_todo(request, todo_id):
    """Edit an existing todo item."""
    todo = get_object_or_404(TodoItem, id=todo_id, user=request.user)
    
    if request.method == 'POST':
        form = TodoItemForm(request.POST, request.FILES, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('todo_list')
    else:
        form = TodoItemForm(instance=todo)
    
    context = {
        'form': form,
        'todo': todo,
        'edit_mode': True,
    }
    return render(request, 'todo_list.html', context)

@login_required
def update_todo_status(request, todo_id):
    """Update the status of a todo item."""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        todo = get_object_or_404(TodoItem, id=todo_id, user=request.user)
        status = request.POST.get('status')
        if status in [choice[0] for choice in TodoItem.STATUS_CHOICES]:
            todo.status = status
            todo.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Invalid status'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def delete_todo(request, todo_id):
    """Delete a todo item."""
    todo = get_object_or_404(TodoItem, id=todo_id, user=request.user)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('todo_list')
    return redirect('todo_list')
