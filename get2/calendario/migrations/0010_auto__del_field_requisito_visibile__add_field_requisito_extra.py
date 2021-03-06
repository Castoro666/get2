# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Requisito.visibile'
        db.delete_column('calendario_requisito', 'visibile')

        # Adding field 'Requisito.extra'
        db.add_column('calendario_requisito', 'extra',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Requisito.visibile'
        db.add_column('calendario_requisito', 'visibile',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Requisito.extra'
        db.delete_column('calendario_requisito', 'extra')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'calendario.disponibilita': {
            'Meta': {'object_name': 'Disponibilita'},
            'creata_da': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creata_da_disponibilita'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mansione': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mansione_disponibilita'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['calendario.Mansione']"}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'persona_disponibilita'", 'to': "orm['calendario.Persona']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'turno': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'turno_disponibilita'", 'to': "orm['calendario.Turno']"}),
            'ultima_modifica': ('django.db.models.fields.DateTimeField', [], {})
        },
        'calendario.gruppo': {
            'Meta': {'object_name': 'Gruppo'},
            'componenti': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'componenti_gruppo'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['calendario.Persona']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'calendario.impostazioni_notifica': {
            'Meta': {'object_name': 'Impostazioni_notifica'},
            'giorni': ('get2.calendario.models.MultiSelectField', [], {'max_length': '250', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo_turno': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['calendario.TipoTurno']", 'null': 'True', 'blank': 'True'}),
            'utente': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'impostazioni_notifica_utente'", 'to': "orm['auth.User']"})
        },
        'calendario.log': {
            'Meta': {'object_name': 'Log'},
            'data': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'testo': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'calendario.mansione': {
            'Meta': {'object_name': 'Mansione'},
            'descrizione': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'calendario.notifica': {
            'Meta': {'object_name': 'Notifica'},
            'data': ('django.db.models.fields.DateTimeField', [], {}),
            'destinatario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'destinatario_user'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'testo': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'calendario.occorrenza': {
            'Meta': {'object_name': 'Occorrenza'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'calendario.persona': {
            'Meta': {'object_name': 'Persona'},
            'cognome': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'competenze': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['calendario.Mansione']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nascita': ('django.db.models.fields.DateField', [], {}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'stato': ('django.db.models.fields.CharField', [], {'default': "'disponibile'", 'max_length': '40'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pers_user'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        },
        'calendario.requisito': {
            'Meta': {'object_name': 'Requisito'},
            'extra': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mansione': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'req_mansione'", 'to': "orm['calendario.Mansione']"}),
            'necessario': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'operatore': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'sufficiente': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tipo_turno': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'req_tipo_turno'", 'to': "orm['calendario.TipoTurno']"}),
            'valore': ('django.db.models.fields.IntegerField', [], {})
        },
        'calendario.tipoturno': {
            'Meta': {'object_name': 'TipoTurno'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identificativo': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'calendario.turno': {
            'Meta': {'object_name': 'Turno'},
            'fine': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identificativo': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'inizio': ('django.db.models.fields.DateTimeField', [], {}),
            'occorrenza': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['calendario.Occorrenza']", 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['calendario.TipoTurno']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['calendario']