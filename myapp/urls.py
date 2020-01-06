from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    # path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    # path(r'<int:book_id>/', views.details, name='details'),
    path(r'findbooks/', views.findbooks, name='findbooks'),
    path(r'place_order/', views.place_order, name='place_order'),
    path(r'review/', views.review_view, name='review'),
    path(r'login/', views.user_login, name='user_login'),
    path(r'logout/', views.user_logout, name='user_logout'),
    path(r'check_reviews/<int:book_id>',views.chk_reviews, name='check_reviews'),
    path(r'register/',views.user_register,name='user_register'),
    path(r'forget/', views.forget, name='forget'),
    path(r'', views.IndexView.as_view(), name='index'),
    path(r'<int:pk>/', views.MyDetailView.as_view(), name='details'),

]

