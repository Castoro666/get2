from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from get2.calendario.models import *
from dajaxice.utils import deserialize_form

@dajaxice_register
def elimina_persona(request,persona_id):
    per=Persona.objects.get(id=persona_id)
    #per.delete()
    dajax = Dajax()
    dajax.remove('#persona-'+str(persona_id))
    return dajax.json()

@dajaxice_register
def elimina_utente(request,utente_id):
    user=User.objects.get(id=utente_id)
    dajax = Dajax()
    if (not user.is_staff() or request.user.is_superuser):
        #user.delete()
        dajax.remove('#utente-'+str(utente_id))
    else:
        pass
    return dajax.json()


@dajaxice_register
def utente_persona(request,user_id,persona_id):
    dajax = Dajax()
    #s=''
    if Persona.objects.filter(user=user_id):
        a=User.objects.get(id=user_id)
        per=Persona.objects.get(user=user_id)
        per.user=None
        per.save()
        if persona_id=='n':
            #s=s+'noty({"text":"l\' utente <b>'+str(a)+'</b> non e piu assegnato a <b>nessun volontario</b>","layout":"bottomRight","type":"success","animateOpen":{"height":"toggle"},"animateClose":{"height":"toggle"},"speed":500,"timeout":5000,"closeButton":true,"closeOnSelfClick":true,"closeOnSelfOver":false});'
            pass

    if persona_id!='n' and User.objects.filter(pers_user=persona_id):
        a=User.objects.get(pers_user=persona_id)
        dajax.assign('select#'+str(a.id),'selectedIndex','0')
        #s=s+'noty({"text":"<b>Attenzione</b>:Il volontario era precedentemente assegnato all\'utente <b>'+str(a)+'</b>","layout":"bottomRight","type":"alert","animateOpen":{"height":"toggle"},"animateClose":{"height":"toggle"},"speed":500,"timeout":5000,"closeButton":true,"closeOnSelfClick":true,"closeOnSelfOver":false});'

    if persona_id!='n':
        per=Persona.objects.get(id=persona_id)
        u=User.objects.get(id=user_id)
        per.user=u
        #s=s+'noty({"text":"Il volontario <b>'+str(vol)+'</b> e stato assegnato all\'utente <b>'+str(u)+'</b>","layout":"bottomRight","type":"success","animateOpen":{"height":"toggle"},"animateClose":{"height":"toggle"},"speed":500,"timeout":5000,"closeButton":true,"closeOnSelfClick":true,"closeOnSelfOver":false});'

    #dajax.script(s)
    per.save()
    return dajax.json()
           
@dajaxice_register
def utente_staff(request,user_id):
    dajax = Dajax()
    u=User.objects.get(id=user_id)
    if request.user.is_superuser:
        if u.is_staff:
            u.is_staff=False
            #dajax.script('noty({"text":"<b>Rimossi</b> i privilegi di staff all\'utente <b>'+str(u)+'</b>","layout":"bottomRight","type":"success","animateOpen":{"height":"toggle"},"animateClose":{"height":"toggle"},"speed":500,"timeout":5000,"closeButton":true,"closeOnSelfClick":true,"closeOnSelfOver":false});')
        else:
            u.is_staff=True
            #dajax.script('noty({"text":"<b>Aggiunti</b> i privilegi di staff all\'utente <b>'+str(u)+'</b>","layout":"bottomRight","type":"success","animateOpen":{"height":"toggle"},"animateClose":{"height":"toggle"},"speed":500,"timeout":5000,"closeButton":true,"closeOnSelfClick":true,"closeOnSelfOver":false});')
        u.save()
    else:
        #dajax.script('noty({"text":"Solo l\'amministratore puo modificare i permessi degli utenti","layout":"bottomRight","type":"error","animateOpen":{"height":"toggle"},"animateClose":{"height":"toggle"},"speed":500,"timeout":5000,"closeButton":true,"closeOnSelfClick":true,"closeOnSelfOver":false});'
        if u.is_staff:
            dajax.assign('input#staff-'+str(user_id),'checked',True)
        else:
            dajax.assign('input#staff-'+str(user_id),'checked',False)          
    return dajax.json()

@dajaxice_register
def notifiche(request,option,url):
    dajax = Dajax()
    i=0
    dajax.assign('#sele','value','')
    for not_id in url.rsplit('_'):
        i+=1
        selector='#not-'+not_id
        m = Notifiche.objects.get(id=not_id)
        
        if (option == 'letto'):
            m.letto=True
            m.save()
            dajax.remove_css_class(selector,'False')
            dajax.add_css_class(selector,'True')
        if (option == 'nonletto'):
            m.letto=False
            m.save()
            dajax.remove_css_class(selector,'True')
            dajax.add_css_class(selector,'False')
        if (option == 'cancella'):
            m.delete()
            dajax.remove(selector)
            dajax.remove('#not-inv-'+not_id)
            #dajax.alert(request.user.get_profile().nonletti())
    dajax.assign('#not_nonlette','innerHTML',request.user.get_profile().nonletti())
    dajax.clear('.ch','checked')
    return dajax.json()


@dajaxice_register
def tipo_turno_form(request, form):
    dajax = Dajax()
    form = TipoTurnoForm(deserialize_form(form))
    if form.is_valid():
        form.save()
        dajax.script('$("#form_tipo_turno" ).dialog("close");')
        html='<div class="riga" id="tipo_turno-'+str(form.cleaned_data.get('id'))+'"><div class="col">'+str(form.cleaned_data.get('identificativo'))+'</div><div class="col">modifica requisiti</div></div><div class="riga" id="requisiti-'+str(form.cleaned_data.get('id'))+'"></div>'
        dajax.append('#elenco', 'innerHTML', html)
        #dajax.alert("aggiunto!")
    else:
        dajax.remove_css_class('#form_tipo_turno input', 'error')
        for error in form.errors:
            dajax.add_css_class('#id_%s' % error, 'ui-state-error')
    return dajax.json()


@dajaxice_register
def requisito_form(request, form):
    dajax = Dajax()
    form = TipoTurnoForm(deserialize_form(form))
    if form.is_valid():
        form.save()
        dajax.script('$("#form_requisito" ).dialog("close");')
        #dajax.append('#elenco', 'innerHTML', html)
        dajax.alert("aggiunto!")
    else:
        dajax.remove_css_class('#form_requisito input', 'error')
        for error in form.errors:
            dajax.add_css_class('#id_%s' % error, 'ui-state-error')
    return dajax.json()
  