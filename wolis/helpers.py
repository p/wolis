import owebunit
import urlparse
from . import utils

xpath_first = owebunit.utils.xpath_first
xpath_first_check = owebunit.utils.xpath_first_check

class Helpers(object):
    def login(self, username, password):
        params = {
            'username': username,
            'password': password,
            'login': 'Login',
        }
        
        self.post('/ucp.php?mode=login', body=params)
        self.assert_successish()
        
        assert 'You have been successfully logged in.' in self.response.body
        
        self.find_sid()
    
    def acp_login(self, username, password):
        self.get_with_sid('/adm/index.php')
        self.assert_successish()
        
        assert 'To administer the board you must re-authenticate yourself.' in self.response.body
        
        assert len(self.response.forms) == 2
        form = self.response.forms[1]
        
        doc = self.response.lxml_etree
        password_name = xpath_first_check(doc, '//input[@type="password"]').attrib['name']
        
        params = {
            'username': username,
            password_name: password,
        }
        
        params = owebunit.extend_params(form.params.list, params)
        self.post(form.computed_action, body=params)
        self.assert_successish()
        
        assert 'You have successfully authenticated' in self.response.body
        
        self.find_sid()
    
    def change_acp_knob(self, link_text, check_page_text, name, value):
        '''Note: requires an estableshed acp session.
        '''
        
        start_url = '/adm/index.php'
        self.get_with_sid(start_url)
        self.assert_successish()
        
        assert 'Board statistics' in self.response.body
        
        url = self.link_href_by_text(link_text)
        
        # already has sid
        self.get(urlparse.urljoin(start_url, url))
        self.assert_successish()
        
        assert check_page_text in self.response.body
        
        assert len(self.response.forms) == 1
        form = self.response.forms[0]
        
        self.check_form_key_delay()
        
        params = {
            name: value,
        }
        params = owebunit.extend_params(form.params.list, params)
        self.post(form.computed_action, body=params)
        self.assert_successish()
        
        assert 'Configuration updated successfully' in self.response.body
