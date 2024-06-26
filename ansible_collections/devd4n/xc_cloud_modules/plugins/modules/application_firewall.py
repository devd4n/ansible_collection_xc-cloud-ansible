#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: application_firewall
short_description: Manage xC Application Firewall
description:
    - WAF Configuration
version_added: "0.0.1"
options:
    metadata:
        annotations:
            description:
                - Annotations is an unstructured key value map stored with a resource
                  that may be set by external tools to store and retrieve arbitrary metadata.
                  They are not queryable and should be preserved when modifying objects.
            type: object
        description:
            description:
                - Human readable description for the object
            type: str
        disable:
            description:
                - A value of true will administratively disable the object
            type: bool
        labels:
            description:
                - Map of string keys and values that can be used to organize and categorize (scope and select)
                  objects as chosen by the user. Values specified here will be used by selector expression
            type: object
        name:
            type: str
            required: True
            description:
                - This is the name of configuration object. It has to be unique within the namespace.
                  It can only be specified during create API and cannot be changed during replace API.
                  The value of name has to follow DNS-1035 format.
        namespace:
            description:
                - This defines the workspace within which each the configuration object is to be created.
                  Must be a DNS_LABEL format
            type: str
    state:
        description:
            - When C(state) is C(present), ensures the object is created or modified.
            - When C(state) is C(absent), ensures the object is removed.
            - When C(state) is C(fetch), returns the object.
        type: str
        choices:
          - present
          - absent
          - fetch
        default: present
    spec:
        allow_all_response_codes:
            type: object (Empty)
            description:
                - This can be used for messages where no values are needed
        allowed_response_codes:
            type: object (Allowed Response Codes)
            description:
                - List of HTTP response status codes that are allowed
        blocking:
            type: object (Empty)
            description:
                - This can be used for messages where no values are needed
        blocking_page:
            type: object (Custom Blocking Page)
            description:
                - Custom blocking response page body
        bot_protection_setting:
            type: object (BotProtectionSetting)
            description:
                - Configuration of WAF Bot Protection
        custom_anonymization:
            type: object (AnonymizationSetting)
            description:
                - Anonymization settings which is a list of HTTP headers, parameters and cookies
        default_anonymization:
            type: object (Empty)
            description:
                - This can be used for messages where no values are needed
        default_bot_setting:
            type: object (Empty)
            description:
                - This can be used for messages where no values are needed
        default_detection_settings:
            type: object (Empty)
            description:
                - This can be used for messages where no values are needed
        detection_settings:
            type: object (Detection Settings)
            description:
                - Specifies detection settings to be used by WAF
        disable_anonymization:
            type: object (Empty)
            description:
                - This can be used for messages where no values are needed
        monitoring:
            type: object (Empty)
            description:
                - This can be used for messages where no values are needed
        use_default_blocking_page:
            type: object (Empty)
            description:
                - This can be used for messages where no values are needed
    patch:
        type: bool
        description: Merge changes with existing on cloud when True
        default: False
'''

EXAMPLES = r'''
---
- name: Configure Application Firewall on XC Cloud
  hosts: webservers
  collections:
    - yoctoalex.xc_cloud_modules
  connection: local

  environment:
    XC_API_TOKEN: "your_api_token"
    XC_TENANT: "console.ves.volterra.io"

  tasks:
    - name: create app firewall
      application_firewall:
        state: present
        metadata:
          namespace: "default"
          name: "demo-fw"
        spec:
          blocking: {}
          detection_settings:
            signature_selection_setting:
              attack_type_settings:
                disabled_attack_types:
                  - "ATTACK_TYPE_COMMAND_EXECUTION"
              high_medium_low_accuracy_signatures: {}
            enable_suppression: { }
            enable_threat_campaigns: { }
            violation_settings:
              disabled_violation_types:
                - "VIOL_HTTP_PROTOCOL_BAD_HTTP_VERSION"
          bot_protection_setting:
            malicious_bot_action: "BLOCK"
            suspicious_bot_action: "REPORT"
            good_bot_action: "REPORT"
          allow_all_response_codes: {}
          default_anonymization: {}
          blocking_page:
            response_code: "Forbidden"
            blocking_page: "string:///yeS5iYWNrKCki....WNrXTwvYT48L2JvZHk+PC9odG1sPg=="
'''

RETURN = r'''
---
metadata:
    annotations:
        description:
            - Annotations is an unstructured key value map stored with a resource
              that may be set by external tools to store and retrieve arbitrary metadata.
              They are not queryable and should be preserved when modifying objects.
        type: object
    description:
        description:
            - Human readable description for the object
        type: str
    disable:
        description:
            - A value of true will administratively disable the object
        type: bool
    labels:
        description:
            - Map of string keys and values that can be used to organize and categorize (scope and select)
              objects as chosen by the user. Values specified here will be used by selector expression
        type: object
    name:
        type: str
        required: True
        description:
            - This is the name of configuration object. It has to be unique within the namespace.
              It can only be specified during create API and cannot be changed during replace API.
              The value of name has to follow DNS-1035 format.
    namespace:
        description:
            - This defines the workspace within which each the configuration object is to be created.
              Must be a DNS_LABEL format
        type: str
spec:
    allow_all_response_codes:
        type: object (Empty)
        description:
            - This can be used for messages where no values are needed
    allowed_response_codes:
        type: object (Allowed Response Codes)
        description:
            - List of HTTP response status codes that are allowed
    blocking:
        type: object (Empty)
        description:
            - This can be used for messages where no values are needed
    blocking_page:
        type: object (Custom Blocking Page)
        description:
            - Custom blocking response page body
    bot_protection_setting:
        type: object (BotProtectionSetting)
        description:
            - Configuration of WAF Bot Protection
    custom_anonymization:
        type: object (AnonymizationSetting)
        description:
            - Anonymization settings which is a list of HTTP headers, parameters and cookies
    default_anonymization:
        type: object (Empty)
        description:
            - This can be used for messages where no values are needed
    default_bot_setting:
        type: object (Empty)
        description:
            - This can be used for messages where no values are needed
    default_detection_settings:
        type: object (Empty)
        description:
            - This can be used for messages where no values are needed
    detection_settings:
        type: object (Detection Settings)
        description:
            - Specifies detection settings to be used by WAF
    disable_anonymization:
        type: object (Empty)
        description:
            - This can be used for messages where no values are needed
    monitoring:
        type: object (Empty)
        description:
            - This can be used for messages where no values are needed
    use_default_blocking_page:
        type: object (Empty)
        description:
            - This can be used for messages where no values are needed
'''

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.client import XcRestClient
from ..module_utils.common import (
    F5ModuleError, AnsibleF5Parameters, f5_argument_spec
)


class Parameters(AnsibleF5Parameters):
    updatables = ['metadata', 'spec']

    returnables = ['metadata', 'spec']

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
    def metadata(self):
        return self._values['metadata']

    @property
    def spec(self):
        return self._values['spec']


class ApiParameters(Parameters):
    @property
    def metadata(self):
        return self._values['metadata']

    @property
    def spec(self):
        return self._values['spec']


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

    def _merge_dicts(self, dict1, dict2):
        for k in set(dict1.keys()).union(dict2.keys()):
            if k in dict1 and k in dict2:
                if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                    yield k, dict(self._merge_dicts(dict1[k], dict2[k]))
                elif dict2[k] is None:
                    pass
                else:
                    yield k, dict2[k]
            elif k in dict1:
                if dict1[k] is None:
                    pass
                else:
                    yield k, dict1[k]
            else:
                if dict2[k] is None:
                    pass
                else:
                    yield k, dict2[k]

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
            return self.update()
        else:
            return self.create()

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        uri = f"/api/config/namespaces/{self.want.metadata['namespace']}/app_firewalls/{self.want.metadata['name']}"
        response = self.client.api.delete(url=uri)
        if response.status == 404:
            return False
        if response.status not in [200, 201, 202]:
            raise F5ModuleError(response.content)

    def exists(self):
        uri = f"/api/config/namespaces/{self.want.metadata['namespace']}/app_firewalls/{self.want.metadata['name']}"
        response = self.client.api.get(url=uri)
        if response.status == 404:
            return False
        if response.status not in [200, 201, 202]:
            raise F5ModuleError(response.content)
        if response.json().get('metadata', None):
            self.have = ApiParameters(params=response.json())
            return True
        return False

    def create(self):
        uri = f"/api/config/namespaces/{self.want.metadata['namespace']}/app_firewalls"
        response = self.client.api.post(url=uri, json=self.want.to_update())
        if response.status not in [200, 201, 202]:
            raise F5ModuleError(response.content)
        self.have = ApiParameters(params=response.json())
        return True

    def update(self):
        if self.want.patch:
            to_update = dict(self._merge_dicts(self.have.to_update(), self.want.to_update()))
        else:
            to_update = self.want.to_update()
        uri = f"/api/config/namespaces/{self.want.metadata['namespace']}/app_firewalls/{self.want.metadata['name']}"
        response = self.client.api.put(url=uri, json=to_update)
        if response.status not in [200, 201, 202]:
            raise F5ModuleError(response.content)
        self.have = ApiParameters(params=to_update)
        return True


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = False

        argument_spec = dict(
            state=dict(
                default='present',
                choices=['present', 'absent', 'fetch']
            ),
            patch=dict(type='bool', default=False),
            metadata=dict(
                type='dict',
                name=dict(required=True),
                namespace=dict(required=True),
                labels=dict(type=dict),
                annotations=dict(type=dict),
                description=dict(type="str"),
                disable=dict(type='bool')
            ),
            spec=dict(
                type=dict,
                allow_all_response_codes=dict(type=dict),
                allowed_response_codes=dict(type=dict),
                blocking=dict(type=dict),
                blocking_page=dict(type=dict),
                bot_protection_setting=dict(type=dict),
                custom_anonymization=dict(type=dict),
                default_anonymization=dict(type=dict),
                default_bot_setting=dict(type=dict),
                default_detection_settings=dict(type=dict),
                detection_settings=dict(type=dict),
                disable_anonymization=dict(type=dict),
                monitoring=dict(type=dict),
                use_default_blocking_page=dict(type=dict),
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
