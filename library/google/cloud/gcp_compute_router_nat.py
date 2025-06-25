#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from googleapiclient.discovery import build
from google.oauth2 import service_account
import traceback

def main():
    module_args = dict(
        project=dict(type='str', required=True),
        name=dict(type='str', required=True),
        router=dict(type='str', required=True),
        region=dict(type='str', required=True),
        nat_ip_allocate_option=dict(type='str', required=True, choices=['AUTO_ONLY']),
        source_subnetwork_ip_ranges_to_nat=dict(type='str', required=True, choices=['ALL_SUBNETWORKS_ALL_IP_RANGES']),
        state=dict(type='str', required=True, choices=['present']),
        service_account_file=dict(type='str', required=True),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    try:
        creds = service_account.Credentials.from_service_account_file(module.params['service_account_file'])
        service = build('compute', 'v1', credentials=creds)

        nat_body = {
            "name": module.params['name'],
            "natIpAllocateOption": module.params['nat_ip_allocate_option'],
            "sourceSubnetworkIpRangesToNat": module.params['source_subnetwork_ip_ranges_to_nat'],
        }

        result = service.routers().get(
            project=module.params['project'],
            region=module.params['region'],
            router=module.params['router']
        ).execute()

        result['nats'] = [nat_body]

        operation = service.routers().patch(
            project=module.params['project'],
            region=module.params['region'],
            router=module.params['router'],
            body=result
        ).execute()

        module.exit_json(changed=True, operation=operation)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())

if __name__ == '__main__':
    main()

