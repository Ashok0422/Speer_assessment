from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, SearchNotesForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Note
from .forms import UserUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
        print(form)
    return render(request, 'api/register.html', {'form': form})


@login_required
def search_notes(request):
    query = request.POST.get('query')
    context =  {'posts' : Note.objects.filter(author=request.user).filter(title__contains=query).order_by('-date_posted')}
    return render(request, 'api/home.html', context)


def home(request):
    context = {
        'posts': Note.objects.all()
    }
    return render(request, 'api/home.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
    }

    return render(request, 'api/profile.html', context)

class PostListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'api/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Note
    template_name = 'api/user_notes.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Note.objects.filter(author=user).order_by('-date_posted')

class PostSearch(ListView):

    model = Note
    fields = ['title']

    form = SearchNotesForm()
    # print('////', form)
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)




    # model = Note
    # template_name = 'api/user_notes.html'  # <app>/<model>_<viewtype>.html
    # context_object_name = 'posts'
    # paginate_by = 5

    # def get_queryset(self):
    #     # user = get_object_or_404(User, username=self.kwargs.get('username'))
    #     form = SearchNotes(self.request.POST)
    #     print('////', form.errors)
    #     if form.is_valid():
    #         text = form.cleaned_data.get('text')

    #     return Note.objects.filter(title__contains=text).order_by('-date_posted')



class PostDetailView(DetailView):
    model = Note


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['title', 'content']
    # print()
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note
    success_url = reverse_lazy('notes-home')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


