# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
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


    def backwards(self, orm):
        # Deleting model 'RelationshipFieldModel'
        db.delete_table(u'core_relationshipfieldmodel')


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
            'this_class': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'regular_fields_set'", 'to': u"orm['core.ClassModel']"})
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
        }
    }

    complete_apps = ['core']