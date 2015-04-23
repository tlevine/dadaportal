from django.db import models

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
        keyword arguments to an ORM update command.
        '''
        raise NotImplementedError

    @classmethod
    def add(Class, filename):
        '''
        Add a new file to the cache.
        '''
        reified = Class.reify(filename)
        if reified != None:
            return Cache.objects.create(**reified)

    def sync(self):
        '''
        Synchronize the cache in the database with the file.
        You must define the class method reify.
        '''

        # If the dates are the same, don't update.
        file_modified = datetime.datetime.fromtimestamp(os.stat(self.filename).st_mtime)
        if self.modified == file_modified:
            return False

        # If the md5sums are the same, update only the date.
        file_md5sum = hashlib.md5(open(self.filename, 'rb').read()).hexdigest()
        if self.md5sum == file_md5sum:
            self.modified == datetime.datetime.now()
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
