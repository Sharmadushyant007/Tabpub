import integ_test_base
import requests
import subprocess
from pathlib import Path


class TestDeployModelSSLOnAuthOff(integ_test_base.IntegTestBase):
    def _get_transfer_protocol(self) -> str:
        return 'https'

    def _get_certificate_file_name(self) -> str:
        return './tests/integration/resources/2019_04_24_to_3018_08_25.crt'

    def _get_key_file_name(self) -> str:
        return './tests/integration/resources/2019_04_24_to_3018_08_25.key'

    def test_deploy_ssl_on_auth_off(self):
        models = ['PCA', 'Sentiment%20Analysis', "ttest"]
        path = str(Path('models', 'setup.py'))
        subprocess.call([self.py, path, self._get_config_file_name()])

        session = requests.Session()
        # Do not verify servers' cert to be signed by trusted CA
        session.verify = False
        # Do not warn about insecure request
        requests.packages.urllib3.disable_warnings()

        for m in models:
            m_response = session.get(url=f'{self._get_transfer_protocol()}://'
                                     f'localhost:9004/endpoints/{m}')
            self.assertEqual(200, m_response.status_code)
