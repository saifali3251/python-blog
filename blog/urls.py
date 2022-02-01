import django
from django.urls import path
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from . import views

app_name = 'blog'

sitemaps = {
  'posts':PostSitemap
}


urlpatterns = [
  # path('',views.PostListView.as_view(),name='post_list'),
  path('',views.homepage,name='homepage'),
  # path('post-list/',views.PostListView.as_view(),name='post_list'),
  path('post-list/',views.post_list,name='post_list'),
  # path('post-search/',views.post_search,name='post_search'),
  path('post/<int:year>/<int:month>/<int:day>/<slug:post>/',views.PostUpdateView.as_view(),name='post_edit'),
  path('draft/',views.draftListView,name='draft_post_list'),
  path('about/',views.post_list,name='about_us'),
  path('tag/<slug:tag_slug>',views.post_list,name='post_list_by_tag'),
  path('<int:year>/<int:month>/<int:day>/<slug:post>',views.post_detail,name='post_detail'),
  path('sitemap.xml',sitemap,{'sitemaps':sitemaps},name='django.contrib.sitemaps.views.sitemap'),
]
