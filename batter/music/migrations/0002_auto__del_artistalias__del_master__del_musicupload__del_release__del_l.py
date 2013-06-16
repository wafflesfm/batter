# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ArtistAlias'
        db.delete_table(u'music_artistalias')

        # Deleting model 'Master'
        db.delete_table(u'music_master')

        # Removing M2M table for field artist_credit on 'Master'
        db.delete_table('music_master_artist_credit')

        # Deleting model 'MusicUpload'
        db.delete_table(u'music_musicupload')

        # Deleting model 'Release'
        db.delete_table(u'music_release')

        # Removing M2M table for field artist_credit on 'Release'
        db.delete_table('music_release_artist_credit')

        # Deleting model 'Label'
        db.delete_table(u'music_label')


    def backwards(self, orm):
        # Adding model 'ArtistAlias'
        db.create_table(u'music_artistalias', (
            ('alias', self.gf('django.db.models.fields.TextField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Artist'])),
        ))
        db.send_create_signal(u'music', ['ArtistAlias'])

        # Adding model 'Master'
        db.create_table(u'music_master', (
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('discogs_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            (u'uploadgroup_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['torrents.UploadGroup'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'music', ['Master'])

        # Adding M2M table for field artist_credit on 'Master'
        db.create_table(u'music_master_artist_credit', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('master', models.ForeignKey(orm[u'music.master'], null=False)),
            ('artist', models.ForeignKey(orm[u'music.artist'], null=False))
        ))
        db.create_unique(u'music_master_artist_credit', ['master_id', 'artist_id'])

        # Adding model 'MusicUpload'
        db.create_table(u'music_musicupload', (
            (u'upload_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['torrents.Upload'], unique=True, primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'_children', to=orm['music.Release'])),
            ('release_format', self.gf('django.db.models.fields.TextField')()),
            ('release', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Release'])),
            ('media', self.gf('django.db.models.fields.TextField')()),
            ('logfile', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('bitrate', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'music', ['MusicUpload'])

        # Adding model 'Release'
        db.create_table(u'music_release', (
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'_children', to=orm['music.Master'])),
            ('discogs_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('label', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Label'])),
            ('release_type', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'music', ['Release'])

        # Adding M2M table for field artist_credit on 'Release'
        db.create_table(u'music_release_artist_credit', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('release', models.ForeignKey(orm[u'music.release'], null=False)),
            ('artist', models.ForeignKey(orm[u'music.artist'], null=False))
        ))
        db.create_unique(u'music_release_artist_credit', ['release_id', 'artist_id'])

        # Adding model 'Label'
        db.create_table(u'music_label', (
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('parent_label', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Label'], null=True, blank=True)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'music', ['Label'])


    models = {
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
        }
    }

    complete_apps = ['music']