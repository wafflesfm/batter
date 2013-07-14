# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MusicUpload'
        db.create_table(u'music_musicupload', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('release', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Release'])),
            ('torrent', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['torrents.Torrent'], unique=True)),
        ))
        db.send_create_signal(u'music', ['MusicUpload'])


    def backwards(self, orm):
        # Deleting model 'MusicUpload'
        db.delete_table(u'music_musicupload')


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
        u'music.musicupload': {
            'Meta': {'object_name': 'MusicUpload'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.Release']"}),
            'torrent': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['torrents.Torrent']", 'unique': 'True'})
        },
        u'music.release': {
            'Meta': {'object_name': 'Release'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.Master']", 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        u'torrents.torrent': {
            'Meta': {'object_name': 'Torrent'},
            'announce': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'announce_list': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'encoding': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'files': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'length': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'md5sum': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'piece_length': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pieces': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['music']