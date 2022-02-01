from re import search
from unittest import result
from django.http import request
from taggit.models import Tag
from django.shortcuts import render,get_object_or_404
from .models import Post
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.views.generic import (ListView,TemplateView,DetailView,CreateView,UpdateView,DeleteView)
from .models import Comment
from .forms import CommentForm,PostForm,SearchForm
from django.db.models import Count

# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'



# class PostListView(ListView):
#   queryset = Post.published.all()
#   context_object_name = 'posts'   #this variable will be used in template file.
#   paginate_by = 3
#   template_name = 'blog/post/list.html'
#   #Django ListView passes page in a variable named page_obj now.


def draftListView(request):
  posts = Post.objects.filter(status='draft')
  return render(request,'blog/post/list.html',{'posts':posts})

  # def get_queryset(self):
      # return Post.objects.filter(status='draft').order_by('created_date')


# def post_search(request):
#   form = SearchForm()
#   query = None
#   results = []
#   if 'query' in request.GET:
#     form = SearchForm(request.GET)
#     if form.is_valid():
#       query = form.cleaned_data['query']
#       print(query)
#       results = Post.published.annotate(
#       search = SearchVector('title','body')
#         ).filter(search=query)
#   return render(request,'blog/post/search.html',{'form':form,'query':query,'results':results})

def post_list(request,tag_slug=None):

  form = SearchForm()
  query = None
  results = []
  if 'query' in request.GET:
    form = SearchForm(request.GET)
    if form.is_valid():
      query = form.cleaned_data['query']
      print(query)
      results = Post.published.annotate(
      search = SearchVector('title','body')
        ).filter(search=query)

  # posts = Post.published.all()
  if results == []:
    object_list = Post.published.all()
  else:
    object_list = results

  tag = None

  if tag_slug:
    tag = get_object_or_404(Tag,slug=tag_slug.lower())
    object_list = object_list.filter(tags__in=[tag])

  paginator = Paginator(object_list,5)
  page = request.GET.get('page')
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    posts = paginator.page(1)
  except EmptyPage:
    posts = paginator.page(paginator.num_pages)


  return render(request,'blog/post/list.html',{'form':form,'query':query,'results':results,'page':page,'posts':posts,'tag':tag})




  # return render(request,'blog/post/search.html',{'form':form,'query':query,'results':results})

# def post_list(request,tag_slug=None):
#   # posts = Post.published.all()
#   object_list = Post.published.all()
#   tag = None

#   if tag_slug:
#     tag = get_object_or_404(Tag,slug=tag_slug.lower())
#     object_list = object_list.filter(tags__in=[tag])

#   paginator = Paginator(object_list,5)
#   page = request.GET.get('page')
#   try:
#     posts = paginator.page(page)
#   except PageNotAnInteger:
#     posts = paginator.page(1)
#   except EmptyPage:
#     posts = paginator.page(paginator.num_pages)
#   return render(request,'blog/post/list.html',{'page':page,'posts':posts,'tag':tag})



def homepage(request,tag_slug=None):
  posts = Post.published.order_by('-publish')[:3]
  object_list = Post.published.all()
  tag = None

  if tag_slug:
    tag = get_object_or_404(Tag,slug=tag_slug.lower())
    object_list = object_list.filter(tags__in=[tag])

  return render(request,'blog/homepage.html',{'posts':posts,'tag':tag})

# class PostDetail(DetailView):
#   model = Post

def post_detail(request,year,month,day,post):
  post = get_object_or_404(Post,slug=post,
                           publish__year=year,
                           publish__month=month,
                           publish__day=day)

  # Comment Part
  comments = post.comments.filter(active=True)
  new_comment = None
  if request.method == 'POST':
    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
      new_comment = comment_form.save(commit=False)
      new_comment.post = post
      new_comment.save()
  else:
    comment_form = CommentForm()

  #List of similar posts
  post_tags_ids = post.tags.values_list('id',flat=True)
  similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                          .exclude(id=post.id)
  similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                        .order_by('-same_tags','-publish')[:4]

  return render(request,'blog/post/detail.html',{'post':post,
                                                  'comments':comments,
                                                  'new_comment':new_comment,
                                                  'comment_form':comment_form,
                                                  'similar_posts':similar_posts})

class PostUpdateView(UpdateView):
  redirect_field_name = 'blog/post/detail.html'
  form_class = PostForm
  model = Post

# def post_search(request):
#   form = SearchForm()
#   query = None


