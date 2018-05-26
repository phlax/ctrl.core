
from zope import component

from .interfaces import IApp, ISettings
from .app import App
from .settings import Settings


component.provideUtility(Settings(), ISettings)
component.provideUtility(App(), IApp)
