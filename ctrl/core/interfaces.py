
from zope.interface import Interface


class ICtrlExtension(Interface):

    def register():
        pass


class ICtrlApp(Interface):

    def setup():
        pass
