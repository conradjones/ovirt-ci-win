import ovirtsdk4.types
import util
import base

connection = base.ovirt_connection()
vms_service = connection.system_service().vms_service()

print('Finding VM')
vm = vms_service.list(search='name=%s' % base.vm_name())[0]
vm_service = vms_service.vm_service(vm.id)

if vm_service.get().status != ovirtsdk4.types.VmStatus.DOWN:
    print('Shutting down VM')
    vm_service.shutdown()

    print('Waiting for VM status')
    if not util.wait_for(lambda: vm_service.get().status == ovirtsdk4.types.VmStatus.DOWN):
        print('Failed')
        exit(1)

print('Deleting VM')
vm_service.remove()
