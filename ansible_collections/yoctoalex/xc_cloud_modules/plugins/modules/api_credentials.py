#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2020, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
'''

EXAMPLES = r'''
---
'''

RETURN = r'''
---
'''

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.client import XcRestClient
from ..module_utils.common import (
    F5ModuleError, AnsibleF5Parameters, f5_argument_spec
)


class Parameters(AnsibleF5Parameters):
    updatables = ['expiration_days', 'name', 'namespace', 'spec']

    returnables = ['data', 'name']

    def to_return(self):
        result = {}
        for returnable in self.returnables:
            result[returnable] = getattr(self, returnable)
        result = self._filter_params(result)
        return result

    def to_update(self):
        result = {}
        for updatebale in self.updatables:
            result[updatebale] = getattr(self, updatebale)
        result = self._filter_params(result)
        return result


class ModuleParameters(Parameters):
    @property
    def expiration_days(self):
        return self._values['metadata']

    @property
    def name(self):
        return self._values['name']

    @property
    def namespace(self):
        return self._values['namespace']

    @property
    def expiration_days(self):
        return self._values['expiration_days']

    @property
    def spec(self):
        return {
            'password': self._values['spec'].get('password', None),
            'type': self._values['spec'].get('api_type', None),
            'virtual_k8s_name': self._values['spec'].get('virtual_k8s_name', None),
            'virtual_k8s_namespace': self._values['spec'].get('virtual_k8s_namespace', None),
        }


class ApiParameters(Parameters):
    @property
    def data(self):
        return self._values['data']

    @property
    def name(self):
        return self._values['name']


class Changes(Parameters):
    def to_return(self):
        result = {}
        try:
            for returnable in self.returnables:
                result[returnable] = getattr(self, returnable)
            result = self._filter_params(result)
        except Exception:
            raise
        return result

    def to_update(self):
        result = {}
        try:
            for updatebale in self.updatables:
                result[updatebale] = getattr(self, updatebale)
            result = self._filter_params(result)
        except Exception:
            raise
        return result


class ModuleManager(object):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.client = XcRestClient(**self.module.params)

        self.want = ModuleParameters(params=self.module.params)
        self.have = ApiParameters()

    def exec_module(self):
        changed = False
        result = dict()
        state = self.want.state

        if state == 'present':
            changed = self.present()
        elif state == 'absent':
            changed = self.absent()
        elif state == 'fetch':
            self.exists()

        changes = self.have.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        return result

    def present(self):
        if self.exists():
            return False
        else:
            return self.create()

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        uri = f"/api/web/namespaces/{self.want.namespace}/revoke/api_credentials"
        response = self.client.api.post(url=uri, json=self.want.to_update())
        if response.status == 404:
            return False
        if response.status not in [200, 201, 202]:
            raise F5ModuleError(response.content)
        return True

    def exists(self):
        uri = f"/api/web/namespaces/{self.want.namespace}/api_credentials/{self.want.name}"
        response = self.client.api.get(url=uri)
        # TODO: server returns 500 error code instead of 404
        if response.status in [404, 500]:
            return False
        if response.status not in [200, 201, 202]:
            raise F5ModuleError(response.content)
        if response.json().get('object', None):
            return True
        return False

    def create(self):
        uri = f"/api/web/namespaces/{self.want.namespace}/api_credentials"
        response = self.client.api.post(url=uri, json=self.want.to_update())
        if response.status not in [200, 201, 202]:
            raise F5ModuleError(response.content)
        self.have = ApiParameters(params=response.json())
        return True


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = False

        argument_spec = dict(
            state=dict(
                default='present',
                choices=['present', 'absent', 'fetch']
            ),
            expiration_days=dict(type='int'),
            name=dict(type='str'),
            namespace=dict(type='str', default='system'),
            spec=dict(
                type=dict,
                password=dict(type=dict),
                api_type=dict(
                    type='str',
                    default='API_CERTIFICATE',
                    choices=[
                        'API_CERTIFICATE',
                        'KUBE_CONFIG',
                        'API_TOKEN',
                        'SERVICE_API_TOKEN',
                        'SERVICE_API_CERTIFICATE',
                        'SERVICE_KUBE_CONFIG',
                        'SITE_GLOBAL_KUBE_CONFIG',
                        'SCIM_API_TOKEN',
                        'SERVICE_SITE_GLOBAL_KUBE_CONFIG'
                    ]
                ),
                virtual_k8s_name=dict(type='str'),
                virtual_k8s_namespace=dict(type='str'),
            )
        )
        self.argument_spec = {}
        self.argument_spec.update(f5_argument_spec)
        self.argument_spec.update(argument_spec)


def main():
    spec = ArgumentSpec()

    module = AnsibleModule(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode
    )
    try:
        mm = ModuleManager(module=module)
        results = mm.exec_module()
        module.exit_json(**results)
    except F5ModuleError as ex:
        module.fail_json(msg=str(ex))


if __name__ == '__main__':
    main()