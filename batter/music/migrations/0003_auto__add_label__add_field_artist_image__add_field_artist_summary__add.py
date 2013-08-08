# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Label'
        db.create_table(u'music_label', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('parent_label', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Label'], null=True, blank=True)),
        ))
        db.send_create_signal(u'music', ['Label'])

        # Adding field 'Artist.image'
        db.add_column(u'music_artist', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Artist.summary'
        db.add_column(u'music_artist', 'summary',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Artist.url'
        db.add_column(u'music_artist', 'url',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Master.image'
        db.add_column(u'music_master', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Master.label'
        db.add_column(u'music_master', 'label',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Label'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Release.slug'
        db.delete_column(u'music_release', 'slug')

        # Adding field 'Release.label'
        db.add_column(u'music_release', 'label',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Label'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Release.year'
        db.add_column(u'music_release', 'year',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Release.catalog_num'
        db.add_column(u'music_release', 'catalog_num',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Release.scene'
        db.add_column(u'music_release', 'scene',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Changing field 'Release.master'
        db.alter_column(u'music_release', 'master_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['music.Master']))

    def backwards(self, orm):
        # Deleting model 'Label'
        db.delete_table(u'music_label')

        # Deleting field 'Artist.image'
        db.delete_column(u'music_artist', 'image')

        # Deleting field 'Artist.summary'
        db.delete_column(u'music_artist', 'summary')

        # Deleting field 'Artist.url'
        db.delete_column(u'music_artist', 'url')

        # Deleting field 'Master.image'
        db.delete_column(u'music_master', 'image')

        # Deleting field 'Master.label'
        db.delete_column(u'music_master', 'label_id')

        # Adding field 'Release.slug'
        db.add_column(u'music_release', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='release', max_length=255),
                      keep_default=False)

        # Deleting field 'Release.label'
        db.delete_column(u'music_release', 'label_id')

        # Deleting field 'Release.year'
        db.delete_column(u'music_release', 'year')

        # Deleting field 'Release.catalog_num'
        db.delete_column(u'music_release', 'catalog_num')

        # Deleting field 'Release.scene'
        db.delete_column(u'music_release', 'scene')


        # Changing field 'Release.master'
        db.alter_column(u'music_release', 'master_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Master'], null=True))

    models = {
        u'music.artist': {
            'Meta': {'object_name': 'Artist'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'music.label': {
            'Meta': {'object_name': 'Label'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'parent_label': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.Label']", 'null': 'True', 'blank': 'True'})
        },
        u'music.master': {
            'Meta': {'object_name': 'Master'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['music.Artist']", 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.Label']", 'null': 'True', 'blank': 'True'}),
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
            'catalog_num': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.Label']", 'null': 'True', 'blank': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.Master']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'scene': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
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