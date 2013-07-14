# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Artist'
        db.create_table(u'music_artist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
        ))
        db.send_create_signal(u'music', ['Artist'])

        # Adding model 'Master'
        db.create_table(u'music_master', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('main', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'+', null=True, to=orm['music.Release'])),
        ))
        db.send_create_signal(u'music', ['Master'])

        # Adding M2M table for field artists on 'Master'
        db.create_table(u'music_master_artists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('master', models.ForeignKey(orm[u'music.master'], null=False)),
            ('artist', models.ForeignKey(orm[u'music.artist'], null=False))
        ))
        db.create_unique(u'music_master_artists', ['master_id', 'artist_id'])

        # Adding model 'Release'
        db.create_table(u'music_release', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Master'], null=True, blank=True)),
        ))
        db.send_create_signal(u'music', ['Release'])


    def backwards(self, orm):
        # Deleting model 'Artist'
        db.delete_table(u'music_artist')

        # Deleting model 'Master'
        db.delete_table(u'music_master')

        # Removing M2M table for field artists on 'Master'
        db.delete_table('music_master_artists')

        # Deleting model 'Release'
        db.delete_table(u'music_release')


    models = {
        u'music.artist': {
            'Meta': {'object_name': 'Artist'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        u'music.master': {
            'Meta': {'object_name': 'Master'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['music.Artist']", 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'+'", 'null': 'True', 'to': u"orm['music.Release']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        u'music.release': {
            'Meta': {'object_name': 'Release'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.Master']", 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['music']