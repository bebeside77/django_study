from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from bookmark.models import Bookmark
from mysite.views import LoginRequiredMixin



# Create your views here.

class BookmarkLV(ListView):
    model = Bookmark


class BookmarkDV(DetailView):
    model = Bookmark


class BookmarkCreateView(LoginRequiredMixin, CreateView):
    model = Bookmark
    fields = ['title', 'url']
    success_url = reverse_lazy('bookmark:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user # 로그인 유저의 정보를 설정함
        return super(BookmarkCreateView, self).form_valid(form)


class BookmarkChangeLV(LoginRequiredMixin, ListView):
    template_name = 'bookmark/bookmark_change_list.html'

    def get_queryset(self): # 대상 가져올 때 실행되는 메소드
        return Bookmark.objects.filter(owner=self.request.user) # 현재 로그인 유저의 데이터만 가져옴


class BookmarkUpdateView(LoginRequiredMixin, UpdateView):
    model = Bookmark
    fields = ['title', 'url']
    success_url = reverse_lazy('bookmark:index')


# get 으로 호출 시 확인 페이지 보여줌 템플릿명은 "모델명_confirm_delete.html"
# post 으로 호출 시 레코드 삭제하고 success_url로 리다이렉트 시킴
class BookmarkDeleteView(LoginRequiredMixin, DeleteView):
    model = Bookmark
    success_url = reverse_lazy('bookmark:index')


