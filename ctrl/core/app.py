
from zope import component, interface
from zope.dottedname.resolve import resolve

from .interfaces import ICtrlApp, ICtrlExtension


@interface.implementer(ICtrlApp)
class CtrlApp(object):

    def discover(self, components):
        for dotted_component in components:
            print('Discovering: %s' % dotted_component)
            resolve(dotted_component)

    async def setup(self, components):
        self.discover(components)
        await self.register_extensions(
            [], component.getUtilitiesFor(ICtrlExtension))

    async def register_extensions(self, loaded, remaining):
        _remaining = []
        for name, extension in remaining:
            for requirement in getattr(extension, 'requires', []):
                if requirement not in loaded:
                    if (name, extension) not in _remaining:
                        _remaining.append((name, extension))
            if (name, extension) in _remaining:
                continue
            loaded.append(name)
            print('Registering extension: %s' % name)
            await extension.register(self)
        if _remaining:
            await self.register_extensions(loaded, _remaining)
