# Copyright 2012 Nebula, Inc.
# Copyright 2013 IBM Corp.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_config import cfg

from nova.api.openstack.compute.contrib import fping as fping_v2
from nova.api.openstack.compute.plugins.v3 import fping
from nova.tests.functional.v3 import test_servers
from nova.tests.unit.api.openstack.compute.contrib import test_fping
from nova import utils

CONF = cfg.CONF
CONF.import_opt('osapi_compute_extension',
                'nova.api.openstack.compute.extensions')


class FpingSampleJsonTests(test_servers.ServersSampleBase):
    extension_name = "os-fping"
    extra_extensions_to_load = ["os-access-ips"]
    _api_version = 'v2'

    def _get_flags(self):
        f = super(FpingSampleJsonTests, self)._get_flags()
        f['osapi_compute_extension'] = CONF.osapi_compute_extension[:]
        f['osapi_compute_extension'].append(
            'nova.api.openstack.compute.contrib.fping.Fping')
        return f

    def setUp(self):
        super(FpingSampleJsonTests, self).setUp()

        def fake_check_fping(self):
            pass
        self.stubs.Set(utils, "execute", test_fping.execute)
        self.stubs.Set(fping.FpingController, "check_fping",
                       fake_check_fping)
        self.stubs.Set(fping_v2.FpingController, "check_fping",
                       fake_check_fping)

    def test_get_fping(self):
        self._post_server()
        response = self._do_get('os-fping')
        subs = self._get_regexes()
        self._verify_response('fping-get-resp', subs, response, 200)

    def test_get_fping_details(self):
        uuid = self._post_server()
        response = self._do_get('os-fping/%s' % (uuid))
        subs = self._get_regexes()
        self._verify_response('fping-get-details-resp', subs, response, 200)
