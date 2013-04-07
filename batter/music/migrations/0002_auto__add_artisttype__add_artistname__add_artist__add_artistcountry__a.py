# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ArtistType'
        db.create_table(u'music_artisttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'music', ['ArtistType'])

        # Adding model 'ArtistName'
        db.create_table(u'music_artistname', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'music', ['ArtistName'])

        # Adding model 'Artist'
        db.create_table(u'music_artist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('mbid', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(related_name='artist_name', to=orm['music.ArtistName'])),
            ('sort_name', self.gf('django.db.models.fields.related.ForeignKey')(related_name='artist_sort_name', to=orm['music.ArtistName'])),
            ('begin_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.ArtistType'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.ArtistCountry'])),
            ('gender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.ArtistGender'])),
            ('disambiguation', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'music', ['Artist'])

        # Adding model 'ArtistCountry'
        db.create_table(u'music_artistcountry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('code', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'music', ['ArtistCountry'])

        # Adding model 'ArtistGender'
        db.create_table(u'music_artistgender', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'music', ['ArtistGender'])


    def backwards(self, orm):
        # Deleting model 'ArtistType'
        db.delete_table(u'music_artisttype')

        # Deleting model 'ArtistName'
        db.delete_table(u'music_artistname')

        # Deleting model 'Artist'
        db.delete_table(u'music_artist')

        # Deleting model 'ArtistCountry'
        db.delete_table(u'music_artistcountry')

        # Deleting model 'ArtistGender'
        db.delete_table(u'music_artistgender')


    models = {
        u'music.artist': {
            'Meta': {'object_name': 'Artist'},
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.ArtistCountry']"}),
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
        u'music.artistcountry': {
            'Meta': {'object_name': 'ArtistCountry'},
            'code': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
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
        }
    }

    complete_apps = ['music']