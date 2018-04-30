from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.views.generic import DetailView,CreateView,TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import *
from . models import *




class RegisterView(CreateView):
	form_class 		= RegisterForm
	template_name 	= 'registration/register.html'
	success_url 	= '/'

	def dispatch(self, *args, **kwargs):
		if self.request.user.is_authenticated():
			return redirect ('/logout')
		return super(RegisterView,self).dispatch(*args, **kwargs)





@login_required()
def add_comment(request,id):
	post = Post.objects.get(id = id)
	form = CommentCreateForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		content = form.cleaned_data['content']
	comment = post.comment_set.create(profile=request.user.profile,post=post,content=content)
	return HttpResponseRedirect(reverse("custom:home"))
	
		



class PostCreateView(LoginRequiredMixin, CreateView):
	# login_url = "/login/"      # I put it in settings
	form_class = PostCreateForm
	template_name = 'form.html'
	success_url = "/"
	
	def form_valid(self,form):
		instance = form.save(commit=False)
		instance.profile = self.request.user.profile
		return super(PostCreateView,self).form_valid(form)

	

	def get_context_data(self, *args, **kwargs):
		context = super(PostCreateView,self).get_context_data(*args, **kwargs)
		context['title'] = 'Add Post'
		return context



class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView,self).get_context_data(*args, **kwargs)

        context['posts'] = Post.objects.all()
        return context


class PostDetail(DetailView):
	model = Post
	template_name = 'custom/post_detail.html'
	context_object_name = 'post'

	def get_context_data(self, *args, **kwargs):
		context = super(PostDetail,self).get_context_data(*args, **kwargs)
		context['form'] = CommentCreateForm()
		return context