from django.urls import path, include
import oauth2_provider.views as oauth2_views
from django.conf import settings
from . import views

###########################################################################################
################################### OAuth 2 Endpoints #####################################
oauth2_endpoint_views = [
    path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token/', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth 2 Configuração de aplicações
    oauth2_endpoint_views += [
        path('applications/', oauth2_views.ApplicationList.as_view(), name="list"),
        path('applications/register/', oauth2_views.ApplicationRegistration.as_view(), name="register"),
        path('applications/<pk>/', oauth2_views.ApplicationDetail.as_view(), name="detail"),
        path('applications/<pk>/delete/', oauth2_views.ApplicationDelete.as_view(), name="delete"),
        path('applications/<pk>/update/', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Configuração de Tokens
    oauth2_endpoint_views += [
        path('authorized-tokens/', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        path('authorized-tokens/<pk>/delete/', oauth2_views.AuthorizedTokenDeleteView.as_view(),
            name="authorized-token-delete"),
    ]

##########################################################################################
###################################### API Endpoints #####################################

urlpatterns = [
    path('auth/', include((oauth2_endpoint_views, 'oauth2_provider'), namespace="oauth2_provider")),
    path('api-auth/', include('rest_framework.urls')),

###########################################################################################
########################################### SET ###########################################
    path('set_exame/', views.setExame, name='set_exame'),
    path('set_exame_arquivo/', views.setExameArquivo.as_view(), name='file-upload'),

###########################################################################################
########################################### GET ###########################################
    path('get_pacientes_lista/', views.getPacientesFHIR, name='pacientes_lista'),
    path('get_paciente/', views.getPaciente, name='paciente'),

    path('get_exames_lista/', views.getExamesLista, name='exames_lista'),
    path('get_exame/', views.getPacienteExameArquivo, name='exames'),
]