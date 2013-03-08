# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from get2.calendario.models import *
from django.shortcuts import render_to_response
import calendar,datetime,locale
from django.db.models import Q, Count, Sum
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AdminPasswordChangeForm 
from django.contrib.auth.decorators import login_required
import pdb
from django.template import RequestContext
from django.forms.formsets import formset_factory
import get2.calendario.settings_calendario as settings_calendario
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test

from eav.models import Attribute #eav import
####   persona   ####

def elenco_persona(request):
	#if request.user.is_staff:
	persone = Persona.objects.all().order_by('cognome')
	gruppi = Gruppo.objects.all()
	mansioni = Mansione.objects.all()
	risposta = HttpResponse(render_to_response('elenco_persona.html',{'persone':persone,'stati':STATI,'request':request,'gruppi':gruppi,'mansioni':mansioni}))
	return risposta
	#else:
	#	return render_to_response('staff-no.html')

@user_passes_test(lambda u:u.is_staff)
def nuovo_persona(request):
	#if request.user.is_staff:
	azione = 'nuovo'
	if request.method == 'POST':
		form = PersonaForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/persone')
	else:
		form = PersonaForm()
	return render_to_response('form_persona.html',{'request':request,'form': form,'azione': azione,'mansione_form':MansioneForm()}, RequestContext(request))
	#else:
	#	return render_to_response('staff-no.html')
	
@user_passes_test(lambda u:u.is_staff)
def modifica_persona(request,persona_id):
	azione = 'modifica'
	per = Persona.objects.get(id=persona_id)
	if request.method == 'POST':  # If the form has been submitted...
		form = PersonaForm(request.POST, instance=per)  # necessario per modificare la riga preesistente
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/persone') # Redirect after POST
	else:
		form = PersonaForm(instance=per)
	return render_to_response('form_persona.html',{'request': request, 'form': form,'azione': azione, 'per': per,'mansione_form':MansioneForm()}, RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def elimina_persona(request,persona_id):
	p=Persona.objects.get(id=persona_id)
	p.delete()
	return HttpResponseRedirect('/persone/')

@user_passes_test(lambda u:u.is_staff)
def nuovo_gruppo(request):
	#if request.user.is_staff:
	azione = 'nuovo'
	if request.method == 'POST':
		form = GruppoForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/persone')
	else:
		form = GruppoForm()
	return render_to_response('form_gruppo.html',{'request':request,'form': form,'azione': azione,}, RequestContext(request))
	#else:
	#	return render_to_response('staff-no.html')
	
@user_passes_test(lambda u:u.is_staff)
def modifica_gruppo(request,gruppo_id):
	azione = 'modifica'
	g = Gruppo.objects.get(id=gruppo_id)
	if request.method == 'POST':  # If the form has been submitted...
		form = GruppoForm(request.POST, instance=g)  # necessario per modificare la riga preesistente
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/persone') # Redirect after POST
	else:
		form = GruppoForm(instance=g)
	return render_to_response('form_gruppo.html',{'request': request, 'form': form,'azione': azione, 'g': g,}, RequestContext(request))

@user_passes_test(lambda u:u.is_staff)
def elimina_gruppo(request,gruppo_id):
	p=Gruppo.objects.get(id=gruppo_id)
	p.delete()
	return HttpResponseRedirect('/persone/')
	
@user_passes_test(lambda u:u.is_staff)
def gruppoaggiungi(request, gruppo_id, per_id):
	g=Gruppo.objects.get(id=gruppo_id)
	p=Persona.objects.get(id=per_id)
	g.componenti.add(v)
	g.save
	return HttpResponseRedirect('/persone/')
	
@user_passes_test(lambda u:u.is_staff)
def gruppoaggiungilista(request):
	#pdb.set_trace()
	if request.GET['gruppo_id']:	
		gruppo_id = request.GET['gruppo_id']
		g=Gruppo.objects.get(id=gruppo_id)
	else:
		return HttpResponseRedirect('/persone/')
	persone = request.GET.getlist('persone_id')
	for per_id in persone:
		if request.GET['azione']=='aggiungi':
			v=Persona.objects.get(id=per_id)
			g.componenti.add(v)
			g.save
		elif request.GET['azione']=='rimuovi':
			v=Persona.objects.get(id=per_id)
			g.componenti.remove(v)
			g.save
	return HttpResponseRedirect('/persone/')

####   fine persona   ####

#####   calendario   ####

def calendario(request):
	if request.COOKIES.has_key('anno'):
		anno=int(request.COOKIES['anno'])
	else:
		anno=datetime.datetime.today().year

	if request.COOKIES.has_key('mese'):
		mese=int(request.COOKIES['mese'])
	else:
		mese=datetime.datetime.today().month

	if request.COOKIES.has_key('giorno'):
		giorno=int(request.COOKIES['giorno'])
	else:
		giorno=datetime.datetime.today().day

	start=datetime.datetime(anno,mese,giorno,1)
	giorni = []
	turni = []
	for i in range(0,7):
		giorni.append(start)
		stop = start + datetime.timedelta(days=1)
		turni.append(Turno.objects.filter(inizio__range=(start, stop)).order_by('inizio'))
		start = start + datetime.timedelta(days=1)
	start = datetime.datetime(anno,mese,giorno,1)
	
	calendario = []
	calendario.append(giorni)
	calendario.append(turni)
	calendario=zip(*calendario)
	tipo_turno=TipoTurno.objects.all()
	gruppi=Gruppo.objects.all()
	corpo=render_to_response('calendario.html',{'calendario':calendario,'start':start,'request':request,'tipo_turno':tipo_turno,'gruppi':gruppi}, RequestContext(request))
	risposta = HttpResponse(corpo)
	risposta.set_cookie('anno', value=anno)
	risposta.set_cookie('mese', value=mese)
	risposta.set_cookie('giorno', value=giorno)
	risposta.set_cookie('sezione', value='calendario')
	return risposta

def calendarioazione(request,azione):
	start = datetime.datetime(int(request.COOKIES['anno']),int(request.COOKIES['mese']),int(request.COOKIES['giorno']))
	if azione == 'oggi':
		start = datetime.datetime.today()
	if azione == 'avanti':
		start += datetime.timedelta(days=1)
	if azione == 'indietro':
		start -= datetime.timedelta(days=1)
	if azione == 'settavanti':
		start += datetime.timedelta(days=7)
	if azione == 'settindietro':
		start -= datetime.timedelta(days=7)
	risposta = HttpResponseRedirect('/calendario/')
	risposta.set_cookie('anno', value=start.year)
	risposta.set_cookie('mese', value=start.month)
	risposta.set_cookie('giorno', value=start.day)
	return risposta
	
@user_passes_test(lambda u:u.is_staff)
def cerca_persona(request, turno_id, mansione_id):
	mansione=Mansione.objects.get(id=mansione_id)
	persone=Persona.objects.filter(competenze=mansione)
	turno=Turno.objects.get(id=turno_id)
	return render_to_response('cerca_persona.html',{'persone':persone,'turno':turno,'mansione':mansione,'DISPONIBILITA':DISPONIBILITA,'request':request})


####   fine calendario   ####

####   disponibilita   ####


def verifica_intervallo(turno):
	now=datetime.datetime.now()
	diff=turno.inizio-now
	if diff.days<0:
		verifica=False
		errore='Turno passato'
	elif diff.days<settings_calendario.DISP_MIN:
		verifica=False
		errore='Troppo vicino (intervallo minore di '+str(settings_calendario.DISP_MIN)+' giorni)'
	elif diff.days>settings_calendario.DISP_MAX:
		verifica=False
		errore='Troppo lontano (intervallo maggiore di '+str(settings_calendario.DISP_MAX)+' giorni)'
	else:
		verifica=True
		errore=''
	return (verifica,errore)


def disponibilita_verifica_tempo(request, turno):
#	pdb.set_trace()
	if request.user.is_staff:
		verifica=True
		errore=''
	else:
		(verifica,errore)=verifica_intervallo(turno)
	#cprint errore
	#print diff.days
	return (verifica,errore)


# attenzione ai permessi
def rimuovi_disponibilita(request, disp_id):
	d=Disponibilita.objects.get(id=disp_id)
	d.tipo='Indisponibile'
	d.save()
	return HttpResponseRedirect('/calendario')

def disponibilita_risolvi_contemporaneo(request,persona_id,contemporaneo):
	if Disponibilita.objects.filter(persona_id=persona_id,turno=contemporaneo).exists():
		for d in Disponibilita.objects.filter(persona_id=persona_id,turno=contemporaneo):
			if d.tipo=="Disponibile":
				persona= Persona.objects.get(id=persona_id)
				notifica_disponibilita(request,persona,contemporaneo,'Non piu disponibile',contemporaneo.mansione)
			rimuovi_disponibilita(d.id)


def nuova_disponibilita(request, turno_id, mansione_id, persona_id, disponibilita):
	#inizializzo ma non salvo un oggetto disponibilita
	#pdb.set_trace()
	disp=Disponibilita()
	disp.tipo=disponibilita
	disp.persona=Persona.objects.get(id=persona_id)
	disp.ultima_modifica=datetime.datetime.now()
	disp.creata_da=request.user
	disp.turno=Turno.objects.get(id=turno_id)
	disp.mansione=Mansione.objects.get(id=mansione_id)
	#verifico se la disponibilita e entro i tempi corretti
	verifica_tempo=disponibilita_verifica_tempo(request, disp.turno)
	if verifica_tempo[0]:
		#una persona puo avere una sola disponibilita per turno
		if Disponibilita.objects.filter(persona=disp.persona,turno=disp.turno ).exists():
			esistente=Disponibilita.objects.get(persona=disp.persona, turno=disp.turno )
			if esistente.tipo=='Disponibile':
				notifica_disponibilita(request,esistente.persona,esistente.turno,'Non piu disponibile',esistente.mansione)
			esistente.delete()
		#risolvo i conflitti con i turni contemporanei
		for contemporaneo in disp.turno.contemporanei():
			disponibilita_risolvi_contemporaneo(request,persona_id,contemporaneo)
		disp.save()
		if not request.user.is_staff:
			notifica_disponibilita(request,disp.persona,disp.turno,disponibilita,disp.mansione)
	return verifica_tempo


def disponibilita_url(request, turno_id, mansione_id, persona_id, disponibilita):
	d=nuova_disponibilita(request, turno_id, mansione_id, persona_id, disponibilita)
	if d[0]:
		return HttpResponseRedirect('/calendario')
	else:
		print d[1]
		
def disponibilita_gruppo(request,turno_id,gruppo_id):
	turno=Turno.objects.get(id=turno_id)
	gruppo=Gruppo.objects.get(id=gruppo_id)
	return render_to_response('disponibilita_gruppo.html',{'turno':turno,'gruppo':gruppo,'request':request})

####   fine disponibilita   ####

####   notifica   ####

def notifica_disponibilita(request,persona,turno,tipo_disponibilita,mansione):
	messaggio='%s si e reso <b> %s </b> con mansione di <b>%s</b> per il turno del<b> %s </b> delle ore<b> %s - %s </b>' % (str(persona), str(tipo_disponibilita),str(mansione), turno.inizio.strftime("%d-%m-%Y"), turno.inizio.strftime("%H:%M"), turno.fine.strftime("%H:%M"))
	now=datetime.datetime.now()
	notifica=Notifica()
	notifica.testo=messaggio
	notifica.data=now
	notifica.letto=False
	if Impostazioni_notifica.objects.filter(giorni__contains=turno.inizio.weekday(),tipo_turno=turno.tipo):
		for i in Impostazioni_notifica.objects.filter(giorni__contains=turno.inizio.weekday(),tipo_turno=turno.tipo):
			#pdb.set_trace()
			notifica.destinatario_id=i.utente.id
			notifica.save()
	else:
		notifica.destinatario_id=1 # se non c'epaola' regola va al admin
		notifica.save()
	return True
	
@user_passes_test(lambda u:u.is_staff)
def elenco_notifica(request):
	u=request.user
	notifiche=Notifica.objects.filter(destinatario=u).order_by('data').reverse()
	return render_to_response('notifiche.html',{'notifiche':notifiche,'request':request})

####   fine notifica   ####

####   inizio utenti   ####
@user_passes_test(lambda u:u.is_staff)
def elenco_utente(request):
	#if request.user.is_staff:
	utenti = User.objects.all()
	persone = Persona.objects.all()
	risposta = HttpResponse(render_to_response('elenco_utente.html',{'utenti':utenti,'persone':persone,'request':request,}))
	return risposta
	#else:
	#	return render_to_response('staff-no.html')
	
@user_passes_test(lambda u:u.is_staff)
def nuovo_utente(request):
	#if request.user.is_staff:
	# Do something for anonymous users.
	azione = 'nuovo';
	if request.method == 'POST': # If the form has been submitted...
		form = UserCreationForm2(request.POST) # A form bound to the POST data
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/utenti/') # Redirect after POST
	else:
		form = UserCreationForm2()
	return render_to_response('form_utente.html',{'request':request, 'form': form,'azione': azione}, RequestContext(request))

@user_passes_test(lambda u:u.is_staff)
def modifica_utente(request,utente_id):
	azione = 'modifica'
	user = User.objects.get(id=utente_id)
	if request.method == 'POST': # If the form has been submitted..
		form = UserChangeForm2(request.POST, instance=user,)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/utenti/') # Redirect after POST
	else:
		form = UserChangeForm2(instance=user)
	return render_to_response('form_utente.html',{'request':request, 'form': form,'azione': azione, 'user': user,}, RequestContext(request))

@user_passes_test(lambda u:u.is_staff)
def modifica_password_utente(request,utente_id):
	user = User.objects.get(id=utente_id)
	if request.method == 'POST': # If the form has been submitted...
		form = AdminPasswordChangeForm(user=user, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/utenti/') # Redirect after POST
	else:
		form = AdminPasswordChangeForm(user=user)
	return render_to_response('form_password_utente.html',{'request':request, 'form': form, 'user': user,}, RequestContext(request))
	
####   fine utenti   ####

#### inizio mansioni ####
@user_passes_test(lambda u: u.is_superuser)
def nuovo_mansione(request):
	azione = 'nuovo'
	if request.method == 'POST': # If the form has been submitted...
		form = MansioneForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/impostazioni') # Redirect after POST
	else:
		form = MansioneForm()
	return render_to_response('form_mansione.html',{'request':request, 'form': form,'azione': azione}, RequestContext(request))	
	
@user_passes_test(lambda u: u.is_superuser)
def modifica_mansione(request, mansione_id):
	azione = 'modifica'
	mansione = Mansione.objects.get(id=mansione_id)
	if request.method == 'POST': # If the form has been submitted...
		form = MansioneForm(request.POST, instance=mansione) # necessario per modificare la riga preesistente
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/impostazioni/') # Redirect after POST
	else:
		form = MansioneForm(instance=mansione)
	return render_to_response('form_mansione.html',{'form':form,'azione': azione, 'mansione': mansione,'request':request}, RequestContext(request))
	
@user_passes_test(lambda u: u.is_superuser)
def elimina_mansione(request,mansione_id):
	m=Mansione.objects.get(id=mansione_id)
	m.delete()
	return HttpResponseRedirect('/impostazioni/')

#### fine mansioni ####

#### inzio tipo turno ####


@user_passes_test(lambda u:u.is_staff)
def impostazioni(request):
	tipi_turno=TipoTurno.objects.all()
	return render_to_response('impostazioni.html',{'tipi_turno':tipi_turno,'tipo_turno_form':TipoTurnoForm(),'operatori':OPERATORI,'mansioni':Mansione.objects.all(),'impostazioni_notifica_utente':Impostazioni_notifica.objects.all(), 'campi_persone':Attribute.objects.all(), 'request':request}, RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def nuovo_tipo_turno(request):
	azione = 'nuovo'
	if request.method == 'POST': # If the form has been submitted...
		tipo_turno_form = TipoTurnoForm(request.POST) # A form bound to the POST data
		if tipo_turno_form.is_valid():
			tipo_turno_form.save()
			return HttpResponseRedirect('/impostazioni/') # Redirect after POST
	else:
		tipo_turno_form = TipoTurnoForm()
	return render_to_response('form_tipo_turno.html',{'tipo_turno_form':tipo_turno_form,'azione':azione,'request':request}, RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def modifica_tipo_turno(request, tipo_turno_id):
	azione = 'modifica';
	tipo_turno = TipoTurno.objects.get(id=tipo_turno_id)
	if request.method == 'POST': # If the form has been submitted...
		tipo_turno_form = TipoTurnoForm(request.POST, instance=tipo_turno) # necessario per modificare la riga preesistente
		if tipo_turno_form.is_valid():
			tipo_turno_form.save()
			return HttpResponseRedirect('/impostazioni/') # Redirect after POST
	else:
		tipo_turno_form = TipoTurnoForm(instance=tipo_turno)
	return render_to_response('form_tipo_turno.html',{'tipo_turno_form': tipo_turno_form,'azione': azione, 'tipo_turno': tipo_turno,'request':request}, RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def elimina_tipo_turno(request,tipo_turno_id):
	t=TipoTurno.objects.get(id=tipo_turno_id)
	t.delete()
	return HttpResponseRedirect('/impostazioni/')

@user_passes_test(lambda u: u.is_superuser)	
def nuovo_impostazioni_notifica(request):
	azione = 'nuovo'
	if request.method == 'POST': # If the form has been submitted...
		impostazioni_notifica_form = Impostazioni_notificaForm(request.POST) # A form bound to the POST data
		if impostazioni_notifica_form.is_valid():
			impostazioni_notifica_form.save()
			return HttpResponseRedirect('/impostazioni/#tabs-notifiche') # Redirect after POST
	else:
		impostazioni_notifica_form = Impostazioni_notificaForm()
	return render_to_response('form_impostazioni_statistiche.html',{'form':impostazioni_notifica_form,'azione':azione,'request':request}, RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def modifica_impostazioni_notifica(request, impostazioni_notifica_id):
	azione = 'modifica';
	impostazioni_notifica = Impostazioni_notifica.objects.get(id=impostazioni_notifica_id)
	if request.method == 'POST': # If the form has been submitted...
		impostazioni_notifica_form = Impostazioni_notificaForm(request.POST, instance=impostazioni_notifica)
		if impostazioni_notifica_form.is_valid():
			impostazioni_notifica_form.save()
			return HttpResponseRedirect('/impostazioni/#tabs-notifiche') # Redirect after POST
	else:
		impostazioni_notifica_form = Impostazioni_notificaForm(instance=impostazioni_notifica)
	return render_to_response('form_impostazioni_statistiche.html',{'form': impostazioni_notifica_form,'azione': azione, 'impostazioni_notifica': impostazioni_notifica,'request':request}, RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def elimina_impostazioni_notifica(request, impostazioni_notifica_id):
	i=Impostazioni_notifica.objects.get(id=impostazioni_notifica_id)
	i.delete()
	return HttpResponseRedirect('/impostazioni/#tabs-notifiche')

#### fine tipo turno ####

#### inizio turno ####
@user_passes_test(lambda u:u.is_staff)
def nuovo_turno(request):
	azione = 'Aggiungi'
	if request.method == 'POST': # If the form has been submitted...
		form = TurnoFormRipeti(request.POST) # A form bound to the POST data
		if form.is_valid():
			data = form.cleaned_data
			form.save()
			if data.get('ripeti'):
				o=Occorrenza()
				o.save()
				start=data.get('ripeti_da')
				stop=data.get('ripeti_al')
				giorno=data.get('ripeti_il_giorno')
				ora_inizio=data.get('inizio').time()
				start=datetime.datetime.combine(start,ora_inizio)
				durata=data.get('fine')-data.get('inizio')
				delta = datetime.timedelta(days=1)
				data['tipo']=data['tipo'].id
				data['occorrenza']=o.id
				#pdb.set_trace()
				while (start.date()<=stop):
					data['inizio_0']=start.date()
					data['fine_0']=(start+durata).date()
					data['inizio_1']=start.time()
					data['fine_1']=(start+durata).time()
					f=TurnoFormRipeti(data)
					if str(start.weekday()) in giorno and f.is_valid():
						t=f.save()
						t.occorrenza=o
						t.save()
					start+=delta
				
			return HttpResponseRedirect('/calendario/') # Redirect after POST
	else:
		form = TurnoFormRipeti()
	return render_to_response('form_turno.html',{'form': form,'azione': azione,'request':request}, RequestContext(request))
	
@user_passes_test(lambda u:u.is_staff)
def modifica_turno(request, turno_id):
	azione = 'Modifica';
	turno = Turno.objects.get(id=turno_id)
	if request.method == 'POST': # If the form has been submitted...
		form = TurnoForm(request.POST, instance=turno) # necessario per modificare la riga preesistente
		if form.is_valid():
			data = form.cleaned_data
			form.save()
			#pdb.set_trace()
			occ=False
			if 'modifica_tutti' in request.POST:
				occorrenze = Turno.objects.filter(occorrenza=turno.occorrenza)
				occ=True
			elif 'modifica_futuri' in request.POST:
				occorrenze = Turno.objects.filter(occorrenza=turno.occorrenza, inizio__gte=turno.inizio)
				occ=True
			if occ:
				for o in occorrenze:
					o.tipo=turno.tipo
					o.valore=turno.valore
					o.identificativo=turno.identificativo
					i=o.inizio.replace(hour=turno.inizio.hour, minute=turno.inizio.minute)
					f=o.fine.replace(hour=turno.fine.hour, minute=turno.fine.minute)
					o.inizio=i
					o.fine=f
					o.save()
			return HttpResponseRedirect('/calendario/') # Redirect after POST
	else:
		form = TurnoForm(instance=turno)
	return render_to_response('form_turno.html',{'form': form,'azione': azione, 'turno': turno,'request':request}, RequestContext(request))

@user_passes_test(lambda u:u.is_staff)
def elimina_turno(request, turno_id):
	t = Turno.objects.get(id=turno_id)
	t.delete()
	return HttpResponseRedirect('/calendario/')

@user_passes_test(lambda u:u.is_staff)
def elimina_turno_occorrenza_succ(request, occorrenza_id):
	o=Occorrenza.objects.get(id=occorrenza_id)
	turni = Turno.objects.filter(occorrenza=o, inizio__gte=datetime.datetime.now())
	for t in turni:
		t.delete()
	return HttpResponseRedirect('/calendario/')

@user_passes_test(lambda u: u.is_superuser)
def elimina_turno_occorrenza(request, occorrenza_id):
	o=Occorrenza.objects.get(id=occorrenza_id)
	turni = Turno.objects.filter(occorrenza=o)
	for t in turni:
		t.delete()
	return HttpResponseRedirect('/calendario/')

#### fine turno ####


#### inizio statistiche ####
elenco_statistiche=("Turni totali",
				"Punteggi totali",
				"Mansioni",
			)

def statistiche(request):
	#se l' intervallo non e specificato prendo tutto
	dati=statistiche_intervallo(request,datetime.date(2000,1,1),datetime.datetime.now().date())
	return render_to_response('statistiche.html',{'dati': dati,'elenco_statistiche':elenco_statistiche,'request':request}, RequestContext(request))

from dateutil.relativedelta import relativedelta



def stat_eta():
	eta=(20,40,60,80,100)
	tot=0
	anno_corrente = datetime.datetime.now()
	for e in eta:
		nato_dopo=anno_corrente- relativedelta(years=e)
		tot=Persona.objects.filter(eav_data_nascita_gte=nato_dopo).count()

def statistiche_intervallo(request, inizio, fine):
	#la funzione calcola le statistiche tra due date, rihiede 2 oggetti datetime.date
	dati=[]
	dati.append(elenco_statistiche)
	stat=[]
	stat.append(Persona.objects.filter(persona_disponibilita__tipo="Disponibile", persona_disponibilita__turno__inizio__gte=inizio, persona_disponibilita__turno__fine__lte=fine ).annotate(tot_turni=Count('persona_disponibilita')).order_by("-tot_turni"))
	stat.append(Persona.objects.filter(persona_disponibilita__tipo="Disponibile", persona_disponibilita__turno__inizio__gte=inizio, persona_disponibilita__turno__fine__lte=fine ).annotate(tot_punti=Sum('persona_disponibilita__turno__valore')).order_by("-tot_punti"))
	stat.append([("x",2),("y",4),("z",8)])
	#pdb.set_trace()
	dati.append(stat)
	dati=zip(*dati)
	#risp=Persona.objects.filter(persona_disponibilita__tipo="Disponibile").annotate(tot_turni=Count('persona_disponibilita'))
	return dati


#### fine statistiche ####

#### inizio requisito ####
@user_passes_test(lambda u: u.is_superuser)
def nuovo_requisito(request,tipo_turno_id):
	t_turno=TipoTurno(id=tipo_turno_id)
	azione = 'nuovo'
	if request.method == 'POST': # If the form has been submitted...
		form = RequisitoForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			r=Requisito(tipo_turno=t_turno)
			form =  RequisitoForm(request.POST, instance=r)
			form.save()
			return HttpResponseRedirect('/impostazioni/#tabs-tipo-turno') # Redirect after POST
	else:
		form = RequisitoForm(initial={'necessario': True,})
	return render_to_response('form_requisito.html',{'request':request, 'tipo_turno': t_turno, 'form': form,'azione': azione}, RequestContext(request))	

@user_passes_test(lambda u: u.is_superuser)
def modifica_requisito(request,requisito_id):
	azione = 'modifica'

	requisito = Requisito.objects.get(id=requisito_id)
	if request.method == 'POST': # If the form has been submitted...
		form = RequisitoForm(request.POST, instance=requisito) # necessario per modificare la riga preesistente
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/impostazioni/#tabs-tipo-turno') # Redirect after POST
	else:
		form = RequisitoForm(instance=requisito)
	return render_to_response('form_requisito.html',{'form':form,'azione': azione,'requisito': requisito,'request':request}, RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def elimina_requisito(request,requisito_id):
	m=Requisito.objects.get(id=requisito_id)
	m.delete()
	return HttpResponseRedirect('/impostazioni/#tabs-tipo-turno')

#### fine requisito ####

#### inizio campo_persone ####
@user_passes_test(lambda u: u.is_superuser)
def nuovo_campo_persone(request):
	azione = 'nuovo'
	if request.method == 'POST': # If the form has been submitted...
		form = AttributeForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/impostazioni/#tabs-persone') # Redirect after POST
	else:
		form = AttributeForm()
	return render_to_response('form_campo_persone.html',{'request':request, 'form': form,'azione': azione}, RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def modifica_campo_persone(request, campo_persone_id):
	azione = 'modifica'
	campo_persone = Attribute.objects.get(id=campo_persone_id)
	if request.method == 'POST': # If the form has been submitted...
		form = AttributeForm(request.POST, instance=campo_persone) # necessario per modificare la riga preesistente
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/impostazioni/#tabs-persone') # Redirect after POST
	else:
		form = AttributeForm(instance=campo_persone)
	return render_to_response('form_campo_persone.html',{'form':form,'azione': azione, 'campo_persone': campo_persone,'request':request}, RequestContext(request))
	

@user_passes_test(lambda u: u.is_superuser)
def elimina_campo_persone(request,campo_persone_id):
	c=Attribute.objects.get(id=campo_persone_id)
	c.delete()
	return HttpResponseRedirect('/impostazioni/#tabs-persone')	

#### fine campo_persone ####


#### inizio pagina persona ####

@user_passes_test(lambda u:u.is_staff)
def visualizza_persona(request,persona_id):
	persona = Persona.objects.get(id=persona_id)
	lista_attributi = eav.models.Entity(Persona).get_all_attributes()
	attributi = {}
	for attributo in lista_attributi:
		try:
			attributi[attributo.slug] = eav.models.Entity(persona).get_value_by_attribute(attributo.id).value
		except: 
  			pass
	return render_to_response('dettaglio_persona.html',{'request': request, 'persona': persona, 'attributi': attributi}, RequestContext(request))

#### fine pagina persona ####
