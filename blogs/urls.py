from django.urls import path, re_path
from . import views

app_name = "blogs"

urlpatterns = [
    path("", views.home, name="home"),
    path('blog/create/', views.BlogCreateView.as_view()),
    path("blog/<slug:the_slug>/edit/",
         views.BlogEditView.as_view(),
         name="edit"),
    path("blog/", views.BlogList.as_view(), name="blog"),
    path('my_blog/', views.my_blog, name='user-blog-list'),
    path("blogs/<slug:the_slug>/",
         views.BlogDetail.as_view(),
         name="blog-detail"),
    path("blog/<slug:the_slug>/delete/",
         views.BlogDeleteView.as_view(),
         name="blog-del"),
]
