# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ArtistCountry'
        db.delete_table(u'music_artistcountry')

        # Adding model 'ArtistCredit'
        db.create_table(u'music_artistcredit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.ArtistName'])),
        ))
        db.send_create_signal(u'music', ['ArtistCredit'])

        # Adding M2M table for field artists on 'ArtistCredit'
        db.create_table(u'music_artistcredit_artists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('artistcredit', models.ForeignKey(orm[u'music.artistcredit'], null=False)),
            ('artist', models.ForeignKey(orm[u'music.artist'], null=False))
        ))
        db.create_unique(u'music_artistcredit_artists', ['artistcredit_id', 'artist_id'])

        # Adding model 'ReleaseName'
        db.create_table(u'music_releasename', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'music', ['ReleaseName'])

        # Adding model 'Country'
        db.create_table(u'music_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('code', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'music', ['Country'])

        # Adding model 'ReleaseGroup'
        db.create_table(u'music_releasegroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('mbid', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.ReleaseName'])),
            ('credit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.ArtistCredit'])),
            ('comment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'music', ['ReleaseGroup'])

        # Adding model 'Release'
        db.create_table(u'music_release', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('mbid', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.ReleaseName'])),
            ('artist_credit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.ArtistCredit'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.ReleaseGroup'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Country'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('barcode', self.gf('django.db.models.fields.TextField')()),
            ('comment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'music', ['Release'])


        # Changing field 'Artist.country'
        db.alter_column(u'music_artist', 'country_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Country']))

    def backwards(self, orm):
        # Adding model 'ArtistCountry'
        db.create_table(u'music_artistcountry', (
            ('code', self.gf('django.db.models.fields.TextField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'music', ['ArtistCountry'])

        # Deleting model 'ArtistCredit'
        db.delete_table(u'music_artistcredit')

        # Removing M2M table for field artists on 'ArtistCredit'
        db.delete_table('music_artistcredit_artists')

        # Deleting model 'ReleaseName'
        db.delete_table(u'music_releasename')

        # Deleting model 'Country'
        db.delete_table(u'music_country')

        # Deleting model 'ReleaseGroup'
        db.delete_table(u'music_releasegroup')

        # Deleting model 'Release'
        db.delete_table(u'music_release')


        # Changing field 'Artist.country'
        db.alter_column(u'music_artist', 'country_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.ArtistCountry']))

    models = {
        u'music.artist': {
            'Meta': {'object_name': 'Artist'},
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.Country']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'disambiguation': ('django.db.models.fields.TextField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.ArtistGender']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mbid': ('django.db.models.fields.TextField', [], {}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'artist_name'", 'to': u"orm['music.ArtistName']"}),
            'sort_name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'artist_sort_name'", 'to': u"orm['music.ArtistName']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.ArtistType']"})
        },
        u'music.artistcredit': {
            'Meta': {'object_name': 'ArtistCredit'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['music.Artist']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.ArtistName']"})
        },
        u'music.artistgender': {
            'Meta': {'object_name': 'ArtistGender'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        u'music.artistname': {
            'Meta': {'object_name': 'ArtistName'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        u'music.artisttype': {
            'Meta': {'object_name': 'ArtistType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        u'music.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        u'music.release': {
            'Meta': {'object_name': 'Release'},
            'artist_credit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.ArtistCredit']"}),
            'barcode': ('django.db.models.fields.TextField', [], {}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.Country']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.ReleaseGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mbid': ('django.db.models.fields.TextField', [], {}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.ReleaseName']"})
        },
        u'music.releasegroup': {
            'Meta': {'object_name': 'ReleaseGroup'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'credit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.ArtistCredit']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mbid': ('django.db.models.fields.TextField', [], {}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.ReleaseName']"})
        },
        u'music.releasename': {
            'Meta': {'object_name': 'ReleaseName'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['music']