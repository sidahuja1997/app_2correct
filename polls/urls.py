from django.conf.urls import url

from . import views
app_name='polls'
urlpatterns = [
url(r'^$',views.dlogin,name='login'),
url(r'^user_login/$',views.user_login,name='user_login'),
url(r'^poster/$',views.poster,name='poster'),
url(r'^post_submit/$',views.poster_submit,name='post_submit'),
url(r'^polls/(?P<user_name>[a-zA-Z]*_?[a-zA-Z]*\d*?)$',views.index,name='index'),
#url(r'^login/',views.login,name='login'),
#url(r'^accept/',views.accept,name='accept'),
url(r'^polls(?P<question_id>[0-9]+)/$',views.detail,name='detail'),
url(r'^polls(?P<question_id>[0-9]+)/results/$',views.results,name='results'),
url(r'^polls(?P<question_id>[0-9]+)/vote/$',views.vote,name='vote'),
#url(r'^login/',views.login,name='login')
 ]
