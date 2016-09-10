from django.shortcuts import render
from django.views.generic import ListView, DetailView, ArchiveIndexView, YearArchiveView, MonthArchiveView, \
    DayArchiveView, TodayArchiveView, TemplateView, FormView
from tagging.views import TaggedObjectList
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from blog.forms import PostSearchForm
from blog.models import Post
from mysite.views import LoginRequireMixin


class PostLV(ListView):
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts'
    paginate_by = 2


class PostTOL(TaggedObjectList):
    model = Post
    template_name = 'blog/tagging/tagging_post_list.html'


class PostDV(DetailView):
    model = Post


class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'modify_date'


class PostYAV(YearArchiveView):
    model = Post
    date_field = 'modify_date'
    make_object_list = True


class PostMAV(MonthArchiveView):
    model = Post
    date_field = 'modify_date'


class PostDAV(DayArchiveView):
    model = Post
    date_field = 'modify_date'


class PostTAV(TodayArchiveView):
    model = Post
    date_field = 'modify_date'


class TagTV(TemplateView):
    template_name = 'blog/tagging/tagging_cloud.html'


class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name = 'blog/post_search.html'

    def form_valid(self, form):
        schWord = '%s' % self.request.POST['search_word']
        post_list = Post.objects.filter(Q(title__icontains=schWord) | Q(description__icontains=schWord)
                                        | Q(content__icontains=schWord)).distinct()

        context = {}
        context['form'] = form
        context['search_term'] = schWord
        context['object_list'] = post_list

        return render(self.request, self.template_name, context) # No Redirection


class PostCreateView(LoginRequireMixin, CreateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tag']
    initial = {'slug': 'auto-filling-do-not-input'}
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user # set login user info
        return super(PostCreateView, self).form_valid(form)


class PostChangeLV(LoginRequireMixin, ListView):
    template_name = 'blog/post_change_list.html'

    def get_queryset(self):
        return Post.objects.filter(owner=self.requet.user) # filter login user's post


class PostUpdateView(LoginRequireMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tag']
    success_url = reverse_lazy('blog:index')


class PostDeleteView(LoginRequireMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')



