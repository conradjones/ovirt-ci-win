import creds
import ovirtsdk4.types
import winrs
import util
import base

connection = base.ovirt_connection()

vms_service = connection.system_service().vms_service()
cluster = ovirtsdk4.types.Cluster(name='Default')
template = ovirtsdk4.types.Template(name='CI-WIN-TEMPLATE')

print('Creating VM')
vm = ovirtsdk4.types.Vm(name=base.vm_name(), template=template, cluster=cluster, delete_protected=False)
vm = vms_service.add(vm)
vm_service = vms_service.vm_service(vm.id)

print('Waiting for VM status')
if not util.wait_for(lambda: vm_service.get().status == ovirtsdk4.types.VmStatus.DOWN):
    print('Failed')
    exit(1)

print('Starting VM')
vm_service.start()

print('Waiting for VM to start')
if not util.wait_for(lambda: vm_service.get().status == ovirtsdk4.types.VmStatus.UP):
    print('Failed')
    exit(1)

print('Waiting for VM IP')
if not util.wait_for(lambda: base.device_ip(vm_service) is not None):
    print('Failed')
    exit(1)

ip = base.device_ip(vm_service)
print("VM IP:%s" % ip)

print('Waiting winRS connection')
remote = winrs.WinRsRemote(host=ip, user=creds.vm_user, auth=creds.vm_password)
if not remote.remoteWaitDeviceIsAwake():
    print('Failed')
    exit(1)

connection.close()
