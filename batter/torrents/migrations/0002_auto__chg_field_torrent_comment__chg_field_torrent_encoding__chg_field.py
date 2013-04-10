# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Torrent.comment'
        db.alter_column(u'torrents_torrent', 'comment', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Torrent.encoding'
        db.alter_column(u'torrents_torrent', 'encoding', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Torrent.created_by'
        db.alter_column(u'torrents_torrent', 'created_by', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Torrent.creation_date'
        db.alter_column(u'torrents_torrent', 'creation_date', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Torrent.comment'
        raise RuntimeError("Cannot reverse this migration. 'Torrent.comment' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Torrent.encoding'
        raise RuntimeError("Cannot reverse this migration. 'Torrent.encoding' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Torrent.created_by'
        raise RuntimeError("Cannot reverse this migration. 'Torrent.created_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Torrent.creation_date'
        raise RuntimeError("Cannot reverse this migration. 'Torrent.creation_date' and its values cannot be restored.")

    models = {
        u'torrents.torrent': {
            'Meta': {'object_name': 'Torrent'},
            'announce': ('django.db.models.fields.TextField', [], {}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'encoding': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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