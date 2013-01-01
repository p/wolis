import owebunit
import urlparse
from wolis_test_case import WolisTestCase

class AcpLoginTestCase(WolisTestCase):
    def test_disable_captcha(self):
        self.login('morpheus', 'morpheus')
        self.acp_login('morpheus', 'morpheus')
        
        self.change_acp_knob(
            link_text='Spambot countermeasures',
            check_page_text='Enable spambot countermeasures',
            name='enable_confirm',
            value='0',
        )
    
    def change_acp_knob(self, link_text, check_page_text, name, value):
        start_url = '/adm/index.php'
        self.get_with_sid(start_url)
        self.assert_status(200)
        
        assert 'Board statistics' in self.response.body
        
        url = self.link_href_by_text(link_text)
        
        # already has sid
        self.get(urlparse.urljoin(start_url, url))
        self.assert_status(200)
        
        assert check_page_text in self.response.body
        
        assert len(self.response.forms) == 1
        form = self.response.forms[0]
        
        params = {
            name: value,
        }
        params = owebunit.extend_params(form.params.list, params)
        self.post(form.computed_action, body=params)
        self.assert_status(200)
        
        assert 'Configuration updated successfully' in self.response.body

if __name__ == '__main__':
    import unittest
    unittest.main()
