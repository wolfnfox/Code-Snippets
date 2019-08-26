import pytest

from helpers import mail

class Tests_MailSender:
    class Tests_init:
        def test_init_raises_Exception(self):
            with pytest.raises(Exception):
                mailsender = mail.MailSender()

        def test_init_loads_mail_settings(self):
            mailsender = mail.MailSender(r'emailsettings.json')
            assert mailsender._connected == False
            assert mailsender._emailsettings is not None
    
    class Tests_connect:
        def test_connect_returns_true_on_connection_success(self):
            mailsender = mail.MailSender(r'emailsettings.json')
            assert mailsender.connect()