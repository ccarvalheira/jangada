# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pip'
        db.create_table(u'core_pip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('installed_apps_text', self.gf('django.db.models.fields.TextField')()),
            ('requirements_pkg_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('requirements_version', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('hard_config', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('soft_config', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Pip'])

        # Adding model 'App'
        db.create_table(u'core_app', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['App'])

        # Adding model 'ClassModel'
        db.create_table(u'core_classmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.App'])),
            ('register_admin', self.gf('django.db.models.fields.BooleanField')()),
            ('is_stacked', self.gf('django.db.models.fields.BooleanField')()),
            ('is_tabular', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'core', ['ClassModel'])

        # Adding model 'FieldModel'
        db.create_table(u'core_fieldmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('this_class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ClassModel'])),
            ('field_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('is_blank', self.gf('django.db.models.fields.BooleanField')()),
            ('is_null', self.gf('django.db.models.fields.BooleanField')()),
            ('is_str', self.gf('django.db.models.fields.BooleanField')()),
            ('list_display', self.gf('django.db.models.fields.BooleanField')()),
            ('filter_on_this', self.gf('django.db.models.fields.BooleanField')()),
            ('search_on_this', self.gf('django.db.models.fields.BooleanField')()),
            ('default', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('editable', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'core', ['FieldModel'])

        # Adding model 'Projecto'
        db.create_table(u'core_projecto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'core', ['Projecto'])

        # Adding M2M table for field used_pips on 'Projecto'
        m2m_table_name = db.shorten_name(u'core_projecto_used_pips')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('projecto', models.ForeignKey(orm[u'core.projecto'], null=False)),
            ('pip', models.ForeignKey(orm[u'core.pip'], null=False))
        ))
        db.create_unique(m2m_table_name, ['projecto_id', 'pip_id'])

        # Adding M2M table for field used_apps on 'Projecto'
        m2m_table_name = db.shorten_name(u'core_projecto_used_apps')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('projecto', models.ForeignKey(orm[u'core.projecto'], null=False)),
            ('app', models.ForeignKey(orm[u'core.app'], null=False))
        ))
        db.create_unique(m2m_table_name, ['projecto_id', 'app_id'])


    def backwards(self, orm):
        # Deleting model 'Pip'
        db.delete_table(u'core_pip')

        # Deleting model 'App'
        db.delete_table(u'core_app')

        # Deleting model 'ClassModel'
        db.delete_table(u'core_classmodel')

        # Deleting model 'FieldModel'
        db.delete_table(u'core_fieldmodel')

        # Deleting model 'Projecto'
        db.delete_table(u'core_projecto')

        # Removing M2M table for field used_pips on 'Projecto'
        db.delete_table(db.shorten_name(u'core_projecto_used_pips'))

        # Removing M2M table for field used_apps on 'Projecto'
        db.delete_table(db.shorten_name(u'core_projecto_used_apps'))


    models = {
        u'core.app': {
            'Meta': {'object_name': 'App'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'core.classmodel': {
            'Meta': {'object_name': 'ClassModel'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.App']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_stacked': ('django.db.models.fields.BooleanField', [], {}),
            'is_tabular': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'register_admin': ('django.db.models.fields.BooleanField', [], {})
        },
        u'core.fieldmodel': {
            'Meta': {'object_name': 'FieldModel'},
            'default': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'editable': ('django.db.models.fields.BooleanField', [], {}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'filter_on_this': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_blank': ('django.db.models.fields.BooleanField', [], {}),
            'is_null': ('django.db.models.fields.BooleanField', [], {}),
            'is_str': ('django.db.models.fields.BooleanField', [], {}),
            'list_display': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'search_on_this': ('django.db.models.fields.BooleanField', [], {}),
            'this_class': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ClassModel']"})
        },
        u'core.pip': {
            'Meta': {'object_name': 'Pip'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hard_config': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'installed_apps_text': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'requirements_pkg_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'requirements_version': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'soft_config': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'core.projecto': {
            'Meta': {'object_name': 'Projecto'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'used_apps': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.App']", 'symmetrical': 'False'}),
            'used_pips': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Pip']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['core']