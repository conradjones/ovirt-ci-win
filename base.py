import ovirtsdk4 as sdk
import ovirtsdk4.types
import creds
import os

# VM
# vm_user = PUT IN CREDS.PY
# vm_password = PUT IN CREDS.PY

# ovirt
# ovirt_url = PUT IN CREDS.PY
# ovirt_user = PUT IN CREDS.PY
# ovirt_password = PUT IN CREDS.PY


script_dir = os.path.dirname(__file__)
ovirt_ca_file = os.path.join(script_dir, 'ca.cer')


def device_ip(vm_service):
    devices_service = vm_service.reported_devices_service()
    devices = devices_service.list(wait=True)

    found_ip = None

    for device in devices:
        for ip in device.ips:
            if ip.version == ovirtsdk4.types.IpVersion.V4:
                found_ip = ip.address

    return found_ip

def ovirt_connection():
    return sdk.Connection(
    url=creds.ovirt_url,
    username=creds.ovirt_user,
    password=creds.ovirt_password,
    ca_file=ovirt_ca_file)

def vm_name():
    return "gitlab-runner-%s-%s-%s-%s" % \
           (os.environ['CUSTOM_ENV_CI_RUNNER_ID'],
            os.environ['CUSTOM_ENV_CI_PROJECT_ID'],
            os.environ['CUSTOM_ENV_CI_CONCURRENT_PROJECT_ID'],
            os.environ['CUSTOM_ENV_CI_JOB_ID'])