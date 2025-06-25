#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: gcp_serviceusage
short_description: Enable or disable a Google Cloud service for a project
description:
  - Allows enabling or disabling a service (API) on a GCP project.
options:
  project:
    description:
      - GCP project ID.
    required: true
    type: str
  service:
    description:
      - Name of the service to enable, e.g. compute.googleapis.com.
    required: true
    type: str
  state:
    description:
      - Desired state of the service.
    choices: [present, absent]
    default: present
    type: str
  auth_kind:
    type: str
    default: serviceaccount
  service_account_file:
    description:
      - Path to the service account key file.
    required: true
    type: str
author:
  - Google LLC
'''

EXAMPLES = r'''
- name: Enable Compute Engine API
  gcp_serviceusage:
    project: my-project
    service: compute.googleapis.com
    service_account_file: /path/to/key.json
'''

RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
import google.auth
from googleapiclient import discovery
from google.oauth2 import service_account


def main():
    module = AnsibleModule(
        argument_spec=dict(
            project=dict(required=True, type='str'),
            service=dict(required=True, type='str'),
            state=dict(default='present', choices=['present', 'absent']),
            auth_kind=dict(type='str', default='serviceaccount'),
            service_account_file=dict(required=True, type='str'),
        ),
        supports_check_mode=True
    )

    project = module.params['project']
    service_name = module.params['service']
    desired_state = module.params['state']
    credentials_path = module.params['service_account_file']

    try:
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        serviceusage = discovery.build('serviceusage', 'v1', credentials=credentials)

        name = f'projects/{project}/services/{service_name}'

        if desired_state == 'present':
            request = serviceusage.services().enable(name=name)
        else:
            request = serviceusage.services().disable(name=name)

        if not module.check_mode:
            request.execute()

        module.exit_json(changed=True, name=name)
    except Exception as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()

