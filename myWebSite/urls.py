from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
#from django.contrib.auth.views import LoginView

from myWebSite.messagingSystem import views as messagingSystem_views
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', messagingSystem_views.index, name='index'),
    url(r'^home/$', messagingSystem_views.home, name='home'),
    url(r'^login/$', auth_views.LoginView.as_view(), {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^signup/$', messagingSystem_views.signup, name='signup'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # url('^', include('django.contrib.auth.urls')),
    url(r'^home/inbox/$', messagingSystem_views.inbox, name='inbox'),
    url(r'^home/outbox/$', messagingSystem_views.outbox, name='outbox'),
    url(r'^home/send/$', messagingSystem_views.send, name='send'),
    url(r'^dbdump/$', messagingSystem_views.dbdump, name='dbdump'),
    url(r'^dbdump/download$', messagingSystem_views.download, name='download'),

]
