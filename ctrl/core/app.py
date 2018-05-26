
import asyncio
import functools
import os
import signal
from collections import OrderedDict

from zope import component, interface
from zope.dottedname.resolve import resolve

from .constants import RUN_FOREVER
from .exceptions import CtrlError
from .interfaces import (
    IApp, ICtrlExtension, ISettings)


@interface.implementer(IApp)
class App(object):

    def __init__(self):
        self.extensions = OrderedDict()

    def discover(self, modules):
        for dotted_name in modules:
            print('Discovering: %s' % dotted_name)
            resolve('%s.extension' % dotted_name)

    def initialize(self, settings_file='/etc/controller.conf', modules=None):
        settings = component.getUtility(ISettings)
        _modules = (
            settings['ctrl'].getlist('modules')
            if 'ctrl' in settings and 'modules' in settings['ctrl']
            else [m for m
                  in os.environ.get('CTRL_MODULES', '').split(',')
                  if m])
        modules = _modules + (modules or [])
        if not modules:
            return
        self.discover(modules)
        extensions = dict(component.getUtilitiesFor(ICtrlExtension))
        try:
            order = self.resolve_extensions(extensions)
        except RecursionError:
            raise CtrlError('Unable to resolve modules: circular dependency')
        for extension in order:
            extensions[extension].register_adapters()
            self.extensions[extension] = extensions[extension]
        return self

    def resolve_extensions(self, extensions, loaded=None):
        loaded = loaded or []
        for name, extension in extensions.items():
            if name in loaded:
                continue
            extension = extensions[name]
            loaded.append(name)
            for requirement in getattr(extension, 'requires', []):
                if requirement not in extensions:
                    raise CtrlError(
                        'Missing dependency %s > %s'
                        % (name, requirement))
                if requirement not in loaded:
                    loaded.pop()
                    break
        if len(loaded) != len(extensions):
            self.resolve_extensions(extensions, loaded)
        return loaded

    async def setup(self, loop=None):
        for name, extension in self.extensions.items():
            await extension.register_utilities()

    def add_signals(self, loop):
        for signame in ('SIGINT', 'SIGTERM'):
            loop.add_signal_handler(
                getattr(signal, signame),
                functools.partial(
                    self.stop, loop, signame))

    def run(self, code, loop=None):
        loop = loop or asyncio.get_event_loop()
        self.add_signals(loop)

        loop.run_until_complete(self.setup(loop))
        response = loop.run_until_complete(code)
        if response is RUN_FOREVER:
            try:
                loop.run_forever()
            finally:
                loop.close()
        loop.close()

    def stop(self, loop, signame):
        print("got signal %s: exit, goodbye..." % signame)
        loop.stop()
