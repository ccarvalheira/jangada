# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EnvProfile'
        db.create_table(u'core_envprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['EnvProfile'])

        # Adding model 'EnvField'
        db.create_table(u'core_envfield', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('env', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.EnvProfile'])),
        ))
        db.send_create_signal(u'core', ['EnvField'])

        # Deleting field 'Project.css_framework'
        db.delete_column(u'core_project', 'css_framework')

        # Adding field 'Project.env_profile'
        db.add_column(u'core_project', 'env_profile',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.EnvProfile']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'EnvProfile'
        db.delete_table(u'core_envprofile')

        # Deleting model 'EnvField'
        db.delete_table(u'core_envfield')


        # User chose to not deal with backwards NULL issues for 'Project.css_framework'
        raise RuntimeError("Cannot reverse this migration. 'Project.css_framework' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Project.css_framework'
        db.add_column(u'core_project', 'css_framework',
                      self.gf('django.db.models.fields.CharField')(max_length=2),
                      keep_default=False)

        # Deleting field 'Project.env_profile'
        db.delete_column(u'core_project', 'env_profile_id')


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
        u'core.envfield': {
            'Meta': {'object_name': 'EnvField'},
            'env': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.EnvProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.envprofile': {
            'Meta': {'object_name': 'EnvProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'syspackages_needed': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'urls_config': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'core.project': {
            'Meta': {'object_name': 'Project'},
            'env_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.EnvProfile']"}),
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