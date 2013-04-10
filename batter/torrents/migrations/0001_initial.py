# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Torrent'
        db.create_table(u'torrents_torrent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('announce', self.gf('django.db.models.fields.TextField')()),
            ('creation_date', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('created_by', self.gf('django.db.models.fields.TextField')()),
            ('encoding', self.gf('django.db.models.fields.TextField')()),
            ('piece_length', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pieces', self.gf('django.db.models.fields.TextField')(unique=True)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('length', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('md5sum', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('files', self.gf('jsonfield.fields.JSONField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'torrents', ['Torrent'])


    def backwards(self, orm):
        # Deleting model 'Torrent'
        db.delete_table(u'torrents_torrent')


    models = {
        u'torrents.torrent': {
            'Meta': {'object_name': 'Torrent'},
            'announce': ('django.db.models.fields.TextField', [], {}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'created_by': ('django.db.models.fields.TextField', [], {}),
            'creation_date': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'encoding': ('django.db.models.fields.TextField', [], {}),
            'files': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'md5sum': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'piece_length': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pieces': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['torrents']