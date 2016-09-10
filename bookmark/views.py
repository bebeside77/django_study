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
        form.instance.owner = self.request_user # 소유자 정보 설정
        return super(BookmarkCreateView, self).form_valid(form)


class BookmarkChangeLV(LoginRequireMixin, ListView):
    template_name = 'bookmark/bookmark_change_list.html'

    def get_queryset(self): # 화면에 출력할 레코드 리스트 반환
        return Bookmark.objects.filter(owner=self.request.user) # 로그인 유저의 데이터만 나오게 함


class BookmarkUpdateView(LoginRequireMixin, UpdateView):
    model = Bookmark
    fields = ['title', 'url']
    success_url = reverse_lazy('bookmark:index')


# 삭제할 것인지 확인하는 페이지를 보여줌
class BookmarkDeleteView(LoginRequireMixin, DeleteView):
    model = Bookmark
    success_url = reverse_lazy('bookmark:index')


