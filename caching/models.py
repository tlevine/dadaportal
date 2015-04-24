import datetime, hashlib, os, logging

from django.db import models

logger = logging.getLogger(__name__)

def _md5sum(filename):
    return hashlib.md5(open(filename, 'rb').read()).hexdigest()

def _modified(filename):
    return datetime.datetime.fromtimestamp(os.stat(filename).st_mtime)

class Cache(models.Model):
    filename = models.TextField(primary_key = True, blank = False)
    modified = models.DateTimeField(null = False)
    md5sum = models.CharField(max_length = 32, null = False)

    class Meta:
        abstract = True

    @staticmethod
    def reify(filename):
        '''
        This should return record fields as a dictionary to be passed as
        keyword arguments to an ORM update command. You must set at least
        any not-null fields that you define.
        '''
        raise NotImplementedError

    @classmethod
    def add(Class, filename):
        '''
        Add a new file to the cache.

        This involves setting the filename, modified, and md5sum, as reify
        doesn't set those.
        '''
        reified = Class.reify(filename)
        if reified == None:
            return

        reified.update({
            'filename': filename,
            'modified': _modified(filename),
            'md5sum': _md5sum(filename),
        })
        return Class.objects.create(**reified)

    def sync(self):
        '''
        Synchronize the cache in the database with the file.
        You must define the class method reify.
        '''

        # If the dates are the same, don't update.
        file_modified = _modified(self.filename)
        if self.modified == file_modified:
            return False
        self.modified = file_modified

        # If the md5sums are the same, update only the date.
        file_md5sum = _md5sum(self.filename)
        if self.md5sum == file_md5sum:
            self.save()
            return False
        self.md5sum = file_md5sum

        # Try to reify.
        reified = self.reify(self.filename)
        if reified == None:
            logger.warn('I could not reify "%s", so I skipped it.' % self.filename)
            self.save()
            return False

        # Update if everything worked.
        for k, v in reified.items():
            setattr(self, k, v)
        self.save()
        return True
