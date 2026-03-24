# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import io

from tests import BaseSessionTest, ClientHTTPStubber


class TestGlacierHandlers(BaseSessionTest):
    def setUp(self):
        super().setUp()
        self.region = 'us-west-2'
        self.client = self.session.create_client('glacier', self.region)
        self.http_stubber = ClientHTTPStubber(self.client)

    def test_can_list_vaults_without_account_id(self):
        with self.http_stubber:
            self.http_stubber.add_response()
            self.client.list_vaults()
            url = self.http_stubber.requests[0].url
            self.assertIn('/-/vaults', url)

    def test_can_list_vaults_with_account_id(self):
        with self.http_stubber:
            self.http_stubber.add_response()
            self.client.list_vaults(accountId='foo')
            url = self.http_stubber.requests[0].url
            self.assertIn('/foo/vaults', url)

    def test_can_upload_archive(self):
        with self.http_stubber:
            self.http_stubber.add_response(status=201)
            self.client.upload_archive(
                vaultName='test-vault',
                body=io.BytesIO(b'bytes content'),
            )
            headers = self.http_stubber.requests[0].headers
            self.assertIn('x-amz-content-sha256', headers)
            self.assertIn('x-amz-sha256-tree-hash', headers)

    def test_can_upload_archive_from_bytes(self):
        with self.http_stubber:
            self.http_stubber.add_response(status=201)
            self.client.upload_archive(
                vaultName='test-vault', body=b'bytes content'
            )
            headers = self.http_stubber.requests[0].headers
            self.assertIn('x-amz-content-sha256', headers)
            self.assertIn('x-amz-sha256-tree-hash', headers)

    def test_glacier_version_header_added(self):
        with self.http_stubber:
            self.http_stubber.add_response()
            self.client.list_vaults()
            headers = self.http_stubber.requests[0].headers
            self.assertIn('x-amz-glacier-version', headers)
