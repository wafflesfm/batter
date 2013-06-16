# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MusicUpload'
        db.create_table(u'music_musicupload', (
            (u'upload_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['torrents.Upload'], unique=True, primary_key=True)),
            ('release', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Release'])),
            ('release_format', self.gf('django.db.models.fields.TextField')()),
            ('bitrate', self.gf('django.db.models.fields.TextField')()),
            ('media', self.gf('django.db.models.fields.TextField')()),
            ('logfile', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'_children', to=orm['music.Release'])),
        ))
        db.send_create_signal(u'music', ['MusicUpload'])

        # Adding model 'Artist'
        db.create_table(u'music_artist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('discogs_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True)),
            ('slug', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('realname', self.gf('django.db.models.fields.TextField')()),
            ('profile', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'music', ['Artist'])

        # Adding model 'ArtistAlias'
        db.create_table(u'music_artistalias', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alias', self.gf('django.db.models.fields.TextField')()),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Artist'])),
        ))
        db.send_create_signal(u'music', ['ArtistAlias'])

        # Adding model 'Release'
        db.create_table(u'music_release', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('discogs_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('label', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Label'])),
            ('release_type', self.gf('django.db.models.fields.TextField')()),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'_children', to=orm['music.Master'])),
        ))
        db.send_create_signal(u'music', ['Release'])

        # Adding M2M table for field artist_credit on 'Release'
        db.create_table(u'music_release_artist_credit', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('release', models.ForeignKey(orm[u'music.release'], null=False)),
            ('artist', models.ForeignKey(orm[u'music.artist'], null=False))
        ))
        db.create_unique(u'music_release_artist_credit', ['release_id', 'artist_id'])

        # Adding model 'Master'
        db.create_table(u'music_master', (
            (u'uploadgroup_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['torrents.UploadGroup'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('discogs_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('comment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'music', ['Master'])

        # Adding M2M table for field artist_credit on 'Master'
        db.create_table(u'music_master_artist_credit', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('master', models.ForeignKey(orm[u'music.master'], null=False)),
            ('artist', models.ForeignKey(orm[u'music.artist'], null=False))
        ))
        db.create_unique(u'music_master_artist_credit', ['master_id', 'artist_id'])

        # Adding model 'Label'
        db.create_table(u'music_label', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('parent_label', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Label'], null=True, blank=True)),
        ))
        db.send_create_signal(u'music', ['Label'])


    def backwards(self, orm):
        # Deleting model 'MusicUpload'
        db.delete_table(u'music_musicupload')

        # Deleting model 'Artist'
        db.delete_table(u'music_artist')

        # Deleting model 'ArtistAlias'
        db.delete_table(u'music_artistalias')

        # Deleting model 'Release'
        db.delete_table(u'music_release')

        # Removing M2M table for field artist_credit on 'Release'
        db.delete_table('music_release_artist_credit')

        # Deleting model 'Master'
        db.delete_table(u'music_master')

        # Removing M2M table for field artist_credit on 'Master'
        db.delete_table('music_master_artist_credit')

        # Deleting model 'Label'
        db.delete_table(u'music_label')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'music.artist': {
            'Meta': {'object_name': 'Artist'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'discogs_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'profile': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'realname': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.TextField', [], {})
        },
        u'music.artistalias': {
            'Meta': {'object_name': 'ArtistAlias'},
            'alias': ('django.db.models.fields.TextField', [], {}),
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.Artist']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'Meta': {'object_name': 'Master', '_ormbases': [u'torrents.UploadGroup']},
            'artist_credit': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['music.Artist']", 'symmetrical': 'False'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'discogs_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'name': ('django.db.models.fields.TextField', [], {}),
            u'uploadgroup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['torrents.UploadGroup']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'music.musicupload': {
            'Meta': {'object_name': 'MusicUpload', '_ormbases': [u'torrents.Upload']},
            'bitrate': ('django.db.models.fields.TextField', [], {}),
            'logfile': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'media': ('django.db.models.fields.TextField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'_children'", 'to': u"orm['music.Release']"}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.Release']"}),
            'release_format': ('django.db.models.fields.TextField', [], {}),
            u'upload_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['torrents.Upload']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'music.release': {
            'Meta': {'object_name': 'Release'},
            'artist_credit': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['music.Artist']", 'symmetrical': 'False'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'discogs_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.Label']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'_children'", 'to': u"orm['music.Master']"}),
            'release_type': ('django.db.models.fields.TextField', [], {})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
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
        },
        u'torrents.upload': {
            'Meta': {'object_name': 'Upload'},
            '_subclass_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'parent_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'parent_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'torrent': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'upload'", 'unique': 'True', 'to': u"orm['torrents.Torrent']"}),
            'upload_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'uploads'", 'to': u"orm['torrents.UploadGroup']"}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'torrents.uploadgroup': {
            'Meta': {'object_name': 'UploadGroup'},
            '_subclass_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        }
    }

    complete_apps = ['music']