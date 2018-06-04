
import os
from collections import OrderedDict
from configparser import ConfigParser

from zope import interface

from .interfaces import ISettings

# move/get rid of this
DEFAULTS = dict(
    apps=[],
    description='',
    services='',
    socket='',
    compose='',
    service='',
    name='',
    daemons='',
    var_path='/var/lib/controller')
DEFAULTS['idle-files'] = ''


class Section(object):

    def __init__(self, section):
        self.section = OrderedDict(section)

    def __getitem__(self, k):
        return self.section[k]

    def __contains__(self, k):
        return k in self.section

    def get(self, k, default=None):
        return self.section.get(k, default)

    def getlist(self, k):
        return self[k].split('\n')


@interface.implementer(ISettings)
class Settings(object):

    def __init__(self):
        self.load()

    def load(self):
        self.config = ConfigParser(DEFAULTS)
        self.config.read(os.environ.get('CFG_CTRL', '/etc/controller.conf'))

    def dump(self):
        pass

    def __getitem__(self, k):
        return Section(self.config.items(k))

    def __contains__(self, k):
        return k in self.config.sections()

    def __iter__(self):
        return iter(self.config.sections())

    def __get(self, k, default=None):
        return self.section.get(k, default)
