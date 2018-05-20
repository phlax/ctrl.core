
from zope import component

from .interfaces import ICtrlApp

from .app import CtrlApp


component.provideUtility(CtrlApp(), ICtrlApp)
