
from zope.interface import Interface


class ISettings(Interface):
    pass


class IApp(Interface):

    def setup():
        pass


class ICtrlExtension(Interface):

    def register():
        pass


class IDatactl(Interface):

    async def list_dbs():
        pass

    async def create_db():
        pass

    async def drop_db():
        pass


class IListener(Interface):

    def listen():
        pass


class IVPNListener(IListener):
    pass


class IVPNctl(Interface):

    def listen():
        pass


class ISystemctl(Interface):

    async def start(service):
        pass

    async def stop(service):
        pass

    async def status(service):
        pass


class IHttpctl(Interface):

    async def start(service):
        pass

    async def stop(service):
        pass

    async def status(service):
        pass


class IServerConfig(Interface):

    pass


class ICtrlConfig(Interface):

    def read():
        pass

    def write():
        pass


class IConfiguration(Interface):

    def configure():
        pass


class ICommandable(Interface):

    def handle(*args):
        pass


class ICommand(Interface):

    def handle(*args):
        pass


class ISubcommand(Interface):

    def handle(*args):
        pass


class ICommandRunner(Interface):

    def handle(*args):
        pass


class IShell(Interface):
    pass


class ICloudctl(Interface):

    async def boot():
        pass

    async def shutdown():
        pass

    async def status(name=None):
        pass


class ICloudProvider(Interface):
    pass


class ICloudSettings(Interface):
    pass


class IFetch(Interface):
    pass
