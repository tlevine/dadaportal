from nikola.plugin_categories import Task
from nikola import utils

from .big import guess_slides

class Big(Task):
    name = 'big'
    def gen_tasks(self):
        pass
