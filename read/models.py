    title = models.TextField(null = True)
    description = models.TextField(null = True)
    body = models.TextField(null = False)

    redirect = models.TextField(null = True)
    tagsjson = models.TextField(null = False) # JSON
    secret = models.BooleanField(null = False, default = False)
    tags
