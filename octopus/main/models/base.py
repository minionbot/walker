# coding: utf-8
# Copyright © 2017  All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now

class BaseModel(models.Model):
    """
    Base model class with common methods for all models.
    """

    created = models.DateTimeField(editable = False, auto_now_add = True)
    modified = models.DateTimeField(default = None, editable = False)
    description = models.TextField(blank = True, default = '')
    active = models.BooleanField(default = True, editable = False)

    class Meta:
        abstract = True

    def __unicode__(self):
        if hasattr(self, 'name'):
            return u'%s-%s' % (self.name, self.id)
        else:
            return u'%s-%s' % (self._meta.verbose_name, self.id)

    def clean_fields(self, exclude = None):
        """
        Override default clean_fields to support methods for cleaning
        individual model fields.
        """
        exclude = exclude or []
        errors = {}
        try:
            super(BaseModel, self).clean_fields(exclude)
        except ValidationError as e:
            errors = e.update_error_dict(errors)

        for f in self._meta.fields:
            if f.name in exclude:
                continue
            if hasattr(self, 'clean_%s' % f.name):
                try:
                    setattr(self, f.name, getattr(self, 'clean_%s' % f.name)())
                except ValidationError as e:
                    errors[f.name] = e.messages

        if errors:
            raise ValidationError(errors)

    def update_fields(self, **kwargs):
        save = kwargs.pop('save', True)
        update_fields = []
        for field, value in kwargs.items():
            if getattr(self, field) != value:
                setattr(self, field, value)
                update_fields.append(field)
        if save and update_fields:
            self.save(update_fields = update_fields)
        return update_fields

    def mark_inactive(self, save = True, update_fields = None, skip_active_check = False):
        """Use instead of delete to rename and mark inactive."""
        update_fields = update_fields or []
        if skip_active_check or self.active:
            dtnow = now()
            if 'name' in self._meta.get_all_field_names():
                self.name = '_deleted_%s_%s' % (dtnow.isoformat(), self.name)
                if 'name' not in update_fields:
                    update_fields.append('name')
            self.active = False
            if 'active' not in update_fields:
                update_fields.append('active')
            if save:
                self.save(update_fields = update_fields)
        return update_fields

    def clean_description(self):
        return self.description or ''

    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields', [])
        if not self.pk and not self.created:
            self.created = now()
            if 'created' not in update_fields:
                update_fields.append('created')
        if 'modified' not in update_fields or not self.modified:
            self.modified = now()
            update_fields.append('modified')

        try:
            super(BaseModel, self).save(*args, **kwargs)
        except TypeError:
            if 'update_fields' not in kwargs:
                raise
            kwargs.pop('update_fields')
            super(BaseModel, self).save(*args, **kwargs)
