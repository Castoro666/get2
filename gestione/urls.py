from django.conf.urls import patterns, include, url

urlpatterns = patterns('gestione',
	# gestione
	(r'^numero_istanze/(?P<classe>\w+)/$', 'views.numero_istanze'),	
	)