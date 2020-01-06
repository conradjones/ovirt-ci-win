import winrs
import sys
import base
import creds

connection = base.ovirt_connection()
vms_service = connection.system_service().vms_service()

vm = vms_service.list(search='name=%s' % base.vm_name())[0]

vm_service = vms_service.vm_service(vm.id)

ip = base.device_ip(vm_service)

remote = winrs.WinRsRemote(host=ip, user=creds.vm_user, auth=creds.vm_password)
if not remote.remoteWaitDeviceIsAwake():
    print('Failed')
    exit(1)

remote.mkdir("c:\\builds")

remote.put(sys.argv[1], "c:\\builds\\script.ps1")

with open(sys.argv[1], "r") as file:
    script = file.read()


if not remote.cmd("powershell -noprofile -noninteractive -executionpolicy Bypass -command c:\\builds\\script.ps1"):
    exit(1)