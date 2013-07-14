# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ArtistAlias'
        db.delete_table(u'music_artistalias')

        # Deleting model 'MusicUpload'
        db.delete_table(u'music_musicupload')

        # Deleting model 'Release'
        db.delete_table(u'music_release')

        # Removing M2M table for field artist_credit on 'Release'
        db.delete_table('music_release_artist_credit')

        # Deleting model 'Label'
        db.delete_table(u'music_label')

        # Deleting field 'Artist.profile'
        db.delete_column(u'music_artist', 'profile')

        # Deleting field 'Artist.discogs_id'
        db.delete_column(u'music_artist', 'discogs_id')

        # Deleting field 'Artist.realname'
        db.delete_column(u'music_artist', 'realname')


        # Changing field 'Artist.slug'
        db.alter_column(u'music_artist', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=255))
        # Adding index on 'Artist', fields ['slug']
        db.create_index(u'music_artist', ['slug'])

        # Deleting field 'Master.comment'
        db.delete_column(u'music_master', 'comment')

        # Deleting field 'Master.discogs_id'
        db.delete_column(u'music_master', 'discogs_id')

        # Deleting field 'Master.uploadgroup_ptr'
        db.delete_column(u'music_master', u'uploadgroup_ptr_id')

        # Adding field 'Master.id'
        db.add_column(u'music_master', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=-1, primary_key=True),
                      keep_default=False)

        # Adding field 'Master.created'
        db.add_column(u'music_master', 'created',
                      self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Master.modified'
        db.add_column(u'music_master', 'modified',
                      self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Master.slug'
        db.add_column(u'music_master', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='master', max_length=255),
                      keep_default=False)

        # Removing M2M table for field artist_credit on 'Master'
        db.delete_table('music_master_artist_credit')

        # Adding M2M table for field artists on 'Master'
        db.create_table(u'music_master_artists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('master', models.ForeignKey(orm[u'music.master'], null=False)),
            ('artist', models.ForeignKey(orm[u'music.artist'], null=False))
        ))
        db.create_unique(u'music_master_artists', ['master_id', 'artist_id'])


    def backwards(self, orm):
        # Removing index on 'Artist', fields ['slug']
        db.delete_index(u'music_artist', ['slug'])

        # Adding model 'ArtistAlias'
        db.create_table(u'music_artistalias', (
            ('alias', self.gf('django.db.models.fields.TextField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Artist'])),
        ))
        db.send_create_signal(u'music', ['ArtistAlias'])

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

        # Adding field 'Artist.profile'
        db.add_column(u'music_artist', 'profile',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Artist.discogs_id'
        raise RuntimeError("Cannot reverse this migration. 'Artist.discogs_id' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Artist.realname'
        raise RuntimeError("Cannot reverse this migration. 'Artist.realname' and its values cannot be restored.")

        # Changing field 'Artist.slug'
        db.alter_column(u'music_artist', 'slug', self.gf('django.db.models.fields.TextField')())

        # User chose to not deal with backwards NULL issues for 'Master.comment'
        raise RuntimeError("Cannot reverse this migration. 'Master.comment' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Master.discogs_id'
        raise RuntimeError("Cannot reverse this migration. 'Master.discogs_id' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Master.uploadgroup_ptr'
        raise RuntimeError("Cannot reverse this migration. 'Master.uploadgroup_ptr' and its values cannot be restored.")
        # Deleting field 'Master.id'
        db.delete_column(u'music_master', u'id')

        # Deleting field 'Master.created'
        db.delete_column(u'music_master', 'created')

        # Deleting field 'Master.modified'
        db.delete_column(u'music_master', 'modified')

        # Deleting field 'Master.slug'
        db.delete_column(u'music_master', 'slug')

        # Adding M2M table for field artist_credit on 'Master'
        db.create_table(u'music_master_artist_credit', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('master', models.ForeignKey(orm[u'music.master'], null=False)),
            ('artist', models.ForeignKey(orm[u'music.artist'], null=False))
        ))
        db.create_unique(u'music_master_artist_credit', ['master_id', 'artist_id'])

        # Removing M2M table for field artists on 'Master'
        db.delete_table('music_master_artists')


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
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['music']