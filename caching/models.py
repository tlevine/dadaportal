from django.db import models

def _md5sum(filename):
    return hashlib.md5(open(filename, 'rb').read()).hexdigest()

def _modified(filename):
    return datetime.datetime.fromtimestamp(os.stat(filename).st_mtime)

class Cache(models.Model):
    endpoint = models.TextField(primary_key = True)
    filename = models.TextField(null = False, blank = False)
    modified = models.DateTimeField(null = False)
    md5sum = models.CharField(max_length = 32, null = False)

    class Meta:
        abstract = True

    @staticmethod
    def reify(filename):
        '''
        This should return record fields as a dictionary to be passed as
        keyword arguments to an ORM update command. You must set at least
        the "endpoint" field and any other not-null fields that you define.
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

        # If the md5sums are the same, update only the date.
        file_md5sum = _md5sum(self.filename)
        if self.md5sum == file_md5sum:
            self.modified == file_modified
            self.save()
            return False

        # Try to reify.
        reified = self.reify(self.filename)
        if reified == None:
            logger.warn('I could not reify "%s", so I skipped it.' % self.filename)
            return False

        # Update if everything worked.
        self.update(**reified)
        return True
