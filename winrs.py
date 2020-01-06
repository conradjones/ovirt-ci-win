from pypsrp.client import Client
from pypsrp.powershell import PowerShell, RunspacePool
from pypsrp.wsman import WSMan
import util


def print_stream(stream):
    for item in stream:
        print(str(item))


def print_error_stream(stream):
    for item in stream:
        print(str(item))
        print(item.script_stacktrace)


def output_powershell_streams(ps):
    print_stream(ps.streams.verbose)
    print_error_stream(ps.streams.error)


class WinRsRemote:

    def __init__(self, *, host=None, user, auth):
        self._host = host
        self._user = user
        self._auth = auth

    def set_host(self, host):
        self._host = host

    def connect(self):
        if self._host is None:
            raise Exception('WinRsRemote host not set')

        try:
            self._client = WSMan(self._host, auth="negotiate", username=self._user, password=self._auth,
                                 ssl=False, connection_timeout=10, read_timeout=900)
            with RunspacePool(self._client) as pool:
                ps = PowerShell(pool)
                ps.add_cmdlet("Get-Process")
                ps.invoke()
        except BaseException as e:
            return False

        return True

    def remoteWaitDeviceIsAwake(self):
        return util.wait_for(lambda: self.connect(), operation_name="remoteDeviceIsAwake",
                             wait_name="Ping %s" % self._host)

    def put(self, source, remote):
        client = Client(self._host, username=self._user, password=self._auth, ssl=False, connection_timeout=10)
        client.copy(source, remote)

    def mkdir(self, path):
        with RunspacePool(self._client) as pool:
            ps = PowerShell(pool)
            ps.add_cmdlet("New-Item").add_parameter("Path", path) \
                .add_parameter("Type", "Directory") \
                .add_parameter("Verbose")

            ps.invoke()
            if ps.had_errors:
                raise Exception(
                    "mkdir:error creating:%s" % path)
            print_stream(ps.streams.verbose)

    def executePowershellScript(self, ps_script):
        client = Client(self._host, username=self._user, password=self._auth, ssl=False, connection_timeout=10)
        output, streams, had_errors = client.execute_ps(ps_script)
        print(output)
        if had_errors:
            print_error_stream(streams.error)
        return not had_errors

    def cmd(self, command):
        client = Client(self._host, username=self._user, password=self._auth, ssl=False, connection_timeout=10)
        out, err, rc = client.execute_cmd(command)
        print("%s" % out)
        if rc != 0:
            print("Error:%s" % err)

        return rc == 0

    @property
    def client(self):
        return self._client

    @property
    def host(self):
        return self._host
