import retry

from pymobiledevice3.lockdown import LockdownClient
from pymobiledevice3.services.dvt.dvt_secure_socket_proxy import DvtSecureSocketProxyService
from pymobiledevice3.exceptions import StartServiceError, ConnectionFailedError

from tart.categories.rpc.rpc import RPC
from tart.categories.apps.apps import Apps
from tart.categories.info.info import Info
from tart.categories.power.power import Power
from tart.categories.files.files import Files
from tart.categories.images.images import Images
from tart.categories.syslog.syslog import Syslog
from tart.categories.browse.browse import Browse
from tart.categories.processes.processes import Processes
from tart.categories.tcp_forward.tcp_forward_manager import TcpForwardManager
from tart.categories.crash.crash import Crash
from tart.categories.browse.module.web_inspector import WebInspector
from tart.log import get_logger
from tart.utils.func_utils import cached_property

log = get_logger()


class Device(object):
    def __init__(self, udid):
        self.udid = udid
        self._lockdown = LockdownClient(udid=udid)
        self._inspector = None

    def __repr__(self):
        return f"<Device '{self.info.model}' {self.info.ios_version}>"

    def __str__(self):
        return self.__repr__()

    @property
    def lockdown(self):
        try:
            self._lockdown.validate_pairing()
        except Exception:
            self._lockdown = LockdownClient(udid=udid)
        return self._lockdown

    @property
    def dvt(self):
        self.images.mount()
        try:
            dvt = DvtSecureSocketProxyService(lockdown=self.lockdown)
            dvt.perform_handshake()
        except (StartServiceError, ConnectionFailedError, BrokenPipeError, ConnectionAbortedError) as e:
            if isinstance(e, (StartServiceError, ConnectionAbortedError)):
                if self.info.ios_version >= self.info.ios_version.create_ios_version('14.0'):
                    self.images.umount()
                self.images.mount()
            dvt = DvtSecureSocketProxyService(lockdown=self.lockdown)
            retry.api.retry_call(dvt.perform_handshake, exceptions=ConnectionAbortedError, tries=2, delay=2, backoff=4)
        return dvt

    @property
    def inspector(self) -> WebInspector:
        if self._inspector:
            self._inspector.close()
        self._inspector = WebInspector(lockdown=self.lockdown)
        return self._inspector

    @property
    def info(self) -> Info:
        return Info(self)

    @cached_property
    def apps(self):
        return Apps(self)

    @cached_property
    def files(self):
        return Files(self)

    @cached_property
    def power(self):
        return Power(self)

    @cached_property
    def syslog(self):
        return Syslog(self)

    @cached_property
    def browse(self):
        return Browse(self)

    @cached_property
    def processes(self):
        return Processes(self)

    @cached_property
    def tcp_forward(self):
        return TcpForwardManager(self)

    @cached_property
    def crash(self):
        return Crash(self)

    @cached_property
    def rpc(self):
        return RPC(self)