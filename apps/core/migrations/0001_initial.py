# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FormModel'
        db.create_table(u'core_formmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.App'])),
            ('output_file', self.gf('django.db.models.fields.CharField')(default='forms.py', max_length=50)),
        ))
        db.send_create_signal(u'core', ['FormModel'])

        # Adding model 'ClassModel'
        db.create_table(u'core_classmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.App'])),
            ('register_admin', self.gf('django.db.models.fields.BooleanField')()),
            ('is_stacked', self.gf('django.db.models.fields.BooleanField')()),
            ('is_tabular', self.gf('django.db.models.fields.BooleanField')()),
            ('output_file', self.gf('django.db.models.fields.CharField')(default='models.py', max_length=50)),
        ))
        db.send_create_signal(u'core', ['ClassModel'])

        # Adding model 'ViewModel'
        db.create_table(u'core_viewmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.App'])),
            ('url_regex', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('override_url_prefix', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('view_type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('form_class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.FormModel'], null=True, blank=True)),
            ('success_url', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.TemplateModel'], null=True, blank=True)),
            ('output_file', self.gf('django.db.models.fields.CharField')(default='views.py', max_length=50)),
        ))
        db.send_create_signal(u'core', ['ViewModel'])

        # Adding model 'RelationshipFieldModel'
        db.create_table(u'core_relationshipfieldmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('is_blank', self.gf('django.db.models.fields.BooleanField')()),
            ('is_null', self.gf('django.db.models.fields.BooleanField')()),
            ('this_class', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relationship_this_class_set', to=orm['core.ClassModel'])),
            ('target_class', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relationship_fields_set', to=orm['core.ClassModel'])),
            ('key_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'core', ['RelationshipFieldModel'])

        # Adding model 'FieldModel'
        db.create_table(u'core_fieldmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('is_blank', self.gf('django.db.models.fields.BooleanField')()),
            ('is_null', self.gf('django.db.models.fields.BooleanField')()),
            ('this_class', self.gf('django.db.models.fields.related.ForeignKey')(related_name='regular_fields_set', to=orm['core.ClassModel'])),
            ('field_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('is_str', self.gf('django.db.models.fields.BooleanField')()),
            ('list_display', self.gf('django.db.models.fields.BooleanField')()),
            ('filter_on_this', self.gf('django.db.models.fields.BooleanField')()),
            ('search_on_this', self.gf('django.db.models.fields.BooleanField')()),
            ('default', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('editable', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'core', ['FieldModel'])

        # Adding model 'FormFieldModel'
        db.create_table(u'core_formfieldmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('is_blank', self.gf('django.db.models.fields.BooleanField')()),
            ('is_null', self.gf('django.db.models.fields.BooleanField')()),
            ('form_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.FormModel'])),
            ('field_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'core', ['FormFieldModel'])

        # Adding model 'Pip'
        db.create_table(u'core_pip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('installed_apps_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('requirements_pkg_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('requirements_version', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('hard_config', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('soft_config', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('syspackages_needed', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Pip'])

        # Adding model 'App'
        db.create_table(u'core_app', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('url_prefix', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('keep_templates', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'core', ['App'])

        # Adding model 'Project'
        db.create_table(u'core_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('css_framework', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal(u'core', ['Project'])

        # Adding M2M table for field used_pips on 'Project'
        m2m_table_name = db.shorten_name(u'core_project_used_pips')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'core.project'], null=False)),
            ('pip', models.ForeignKey(orm[u'core.pip'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'pip_id'])

        # Adding M2M table for field used_apps on 'Project'
        m2m_table_name = db.shorten_name(u'core_project_used_apps')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'core.project'], null=False)),
            ('app', models.ForeignKey(orm[u'core.app'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'app_id'])

        # Adding model 'TemplateModel'
        db.create_table(u'core_templatemodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('is_base', self.gf('django.db.models.fields.BooleanField')()),
            ('extend', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.TemplateModel'], null=True, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Project'], null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['TemplateModel'])

        # Adding model 'TemplateBlock'
        db.create_table(u'core_templateblock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.TemplateModel'])),
            ('block_type', self.gf('django.db.models.fields.CharField')(default='body', max_length=6)),
        ))
        db.send_create_signal(u'core', ['TemplateBlock'])


    def backwards(self, orm):
        # Deleting model 'FormModel'
        db.delete_table(u'core_formmodel')

        # Deleting model 'ClassModel'
        db.delete_table(u'core_classmodel')

        # Deleting model 'ViewModel'
        db.delete_table(u'core_viewmodel')

        # Deleting model 'RelationshipFieldModel'
        db.delete_table(u'core_relationshipfieldmodel')

        # Deleting model 'FieldModel'
        db.delete_table(u'core_fieldmodel')

        # Deleting model 'FormFieldModel'
        db.delete_table(u'core_formfieldmodel')

        # Deleting model 'Pip'
        db.delete_table(u'core_pip')

        # Deleting model 'App'
        db.delete_table(u'core_app')

        # Deleting model 'Project'
        db.delete_table(u'core_project')

        # Removing M2M table for field used_pips on 'Project'
        db.delete_table(db.shorten_name(u'core_project_used_pips'))

        # Removing M2M table for field used_apps on 'Project'
        db.delete_table(db.shorten_name(u'core_project_used_apps'))

        # Deleting model 'TemplateModel'
        db.delete_table(u'core_templatemodel')

        # Deleting model 'TemplateBlock'
        db.delete_table(u'core_templateblock')


    models = {
        u'core.app': {
            'Meta': {'object_name': 'App'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keep_templates': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url_prefix': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'core.classmodel': {
            'Meta': {'object_name': 'ClassModel'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.App']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_stacked': ('django.db.models.fields.BooleanField', [], {}),
            'is_tabular': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'output_file': ('django.db.models.fields.CharField', [], {'default': "'models.py'", 'max_length': '50'}),
            'register_admin': ('django.db.models.fields.BooleanField', [], {})
        },
        u'core.fieldmodel': {
            'Meta': {'object_name': 'FieldModel'},
            'default': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'editable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'filter_on_this': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_blank': ('django.db.models.fields.BooleanField', [], {}),
            'is_null': ('django.db.models.fields.BooleanField', [], {}),
            'is_str': ('django.db.models.fields.BooleanField', [], {}),
            'list_display': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'search_on_this': ('django.db.models.fields.BooleanField', [], {}),
            'this_class': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'regular_fields_set'", 'to': u"orm['core.ClassModel']"})
        },
        u'core.formfieldmodel': {
            'Meta': {'object_name': 'FormFieldModel'},
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'form_model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.FormModel']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_blank': ('django.db.models.fields.BooleanField', [], {}),
            'is_null': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'core.formmodel': {
            'Meta': {'object_name': 'FormModel'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.App']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'output_file': ('django.db.models.fields.CharField', [], {'default': "'forms.py'", 'max_length': '50'})
        },
        u'core.pip': {
            'Meta': {'object_name': 'Pip'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hard_config': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'installed_apps_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'requirements_pkg_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'requirements_version': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'soft_config': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'syspackages_needed': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'core.project': {
            'Meta': {'object_name': 'Project'},
            'css_framework': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'used_apps': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.App']", 'symmetrical': 'False'}),
            'used_pips': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Pip']", 'symmetrical': 'False'})
        },
        u'core.relationshipfieldmodel': {
            'Meta': {'object_name': 'RelationshipFieldModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_blank': ('django.db.models.fields.BooleanField', [], {}),
            'is_null': ('django.db.models.fields.BooleanField', [], {}),
            'key_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'target_class': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relationship_fields_set'", 'to': u"orm['core.ClassModel']"}),
            'this_class': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relationship_this_class_set'", 'to': u"orm['core.ClassModel']"})
        },
        u'core.templateblock': {
            'Meta': {'object_name': 'TemplateBlock'},
            'block_type': ('django.db.models.fields.CharField', [], {'default': "'body'", 'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.TemplateModel']"})
        },
        u'core.templatemodel': {
            'Meta': {'object_name': 'TemplateModel'},
            'extend': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.TemplateModel']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_base': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Project']", 'null': 'True', 'blank': 'True'})
        },
        u'core.viewmodel': {
            'Meta': {'object_name': 'ViewModel'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.App']"}),
            'form_class': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.FormModel']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'output_file': ('django.db.models.fields.CharField', [], {'default': "'views.py'", 'max_length': '50'}),
            'override_url_prefix': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'success_url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.TemplateModel']", 'null': 'True', 'blank': 'True'}),
            'url_regex': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'view_type': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['core']