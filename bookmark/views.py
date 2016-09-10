from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from bookmark.models import Bookmark
from mysite.views import LoginRequireMixin


# Create your views here.

class BookmarkLV(ListView):
    model = Bookmark


class BookmarkDV(DetailView):
    model = Bookmark


class BookmarkCreateView(LoginRequireMixin, CreateView):
    model = Bookmark
    fields = ['title', 'url']
    success_url = reverse_lazy('bookmark:index')

    def form_valid(self, form):
        form.instance.owner = self.request_user # ������ ���� ����
        return super(BookmarkCreateView, self).form_valid(form)


class BookmarkChangeLV(LoginRequireMixin, ListView):
    template_name = 'bookmark/bookmark_change_list.html'

    def get_queryset(self): # ȭ�鿡 ����� ���ڵ� ����Ʈ ��ȯ
        return Bookmark.objects.filter(owner=self.request.user) # �α��� ������ �����͸� ������ ��


class BookmarkUpdateView(LoginRequireMixin, UpdateView):
    model = Bookmark
    fields = ['title', 'url']
    success_url = reverse_lazy('bookmark:index')


# ������ ������ Ȯ���ϴ� �������� ������
class BookmarkDeleteView(LoginRequireMixin, DeleteView):
    model = Bookmark
    success_url = reverse_lazy('bookmark:index')


