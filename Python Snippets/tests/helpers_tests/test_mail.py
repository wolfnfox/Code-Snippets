import pytest
import socket

from helpers import mail

test_email_settings = r'./helpers/config/emailsettings.json'
test_email_settings_invalid_host = r'./helpers/config/emailsettings-invalidhost.json'
test_email_settings_wrong_password = r'./helpers/config/emailsettings-wrongpassword.json'

class Tests_MailReceiver:
    class Tests_init:
        def test_raises_Exception_if_no_settings(self):
            with pytest.raises(Exception):
                mailreceiver = mail.MailReceiver()

        def test_loads_mail_settings(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            assert mailreceiver._connected == False
            assert mailreceiver._mailboxopen == None
            assert mailreceiver.download_options is not None
            assert isinstance(mailreceiver.download_options.filter_by_extension,list)
            assert mailreceiver.download_options.greater_than_size_kb == 0
            assert mailreceiver._email_settings is not None

    class Tests_connect:
        def test_returns_true_on_connection_success(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            assert mailreceiver.connect()

        def test_returns_true_if_already_connected(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            mailreceiver.connect()
            assert mailreceiver.connect()

        def test_raises_Exception_if_invalid_host(self):
            mailreceiver = mail.MailReceiver(test_email_settings_invalid_host)
            with pytest.raises(socket.gaierror):
                mailreceiver.connect()

        def test_raises_Exception_if_wrong_credentials(self):
            mailreceiver = mail.MailReceiver(test_email_settings_wrong_password)
            with pytest.raises(Exception):
                mailreceiver.connect()

    class Tests_open_mailbox:
        def test_returns_true_on_success(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            mailreceiver.connect()
            assert not mailreceiver._mailboxopen
            assert mailreceiver.open_mailbox('Inbox')

        def test_returns_true_when_changing_mailbox_implicitly(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            mailreceiver.connect()
            assert not mailreceiver._mailboxopen
            assert mailreceiver.open_mailbox('Inbox')
            assert mailreceiver.open_mailbox('Inbox')

        def test_returns_true_when_changing_mailbox_explicitly(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            mailreceiver.connect()
            assert not mailreceiver._mailboxopen
            assert mailreceiver.open_mailbox('Inbox')
            assert mailreceiver.close_mailbox()
            assert mailreceiver.open_mailbox('Inbox')
    
    class Tests_close_mailbox:
        def test_returns_true_on_success(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            mailreceiver.connect()
            assert mailreceiver.open_mailbox('Inbox')
            assert mailreceiver.close_mailbox()

        def test_returns_true_if_already_closed(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            mailreceiver.connect()
            assert mailreceiver.close_mailbox()

        @pytest.mark.parametrize('num',[2,3,9])
        def test_returns_true_for_multiple_open_close(self,num):
            mailreceiver = mail.MailReceiver(test_email_settings)
            mailreceiver.connect()
            for i in range(num):
                mailreceiver.open_mailbox('Inbox')
                assert mailreceiver.close_mailbox()

    class Tests_get_all_mailids:
        def test_raises_Exception_if_no_mailbox_open(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            mailreceiver.connect()
            with pytest.raises(Exception):
                mailreceiver.get_all_mailids()

        def test_returns_list_of_mailids_from_currently_open_mailbox(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            mailreceiver.connect()
            mailreceiver.open_mailbox('Inbox')
            mailids = mailreceiver.get_all_mailids()
            assert isinstance(mailids,list)
            assert isinstance(mailids[0],bytes)

        def test_returns_list_of_mailids_from_specified_mailbox(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            mailreceiver.connect()
            mailids = mailreceiver.get_all_mailids('Inbox')
            assert isinstance(mailids,list)
            assert isinstance(mailids[0],bytes)

        def test_returns_empty_list_from_empty_mailbox(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            mailreceiver.connect()
            mailids = mailreceiver.get_all_mailids('Trash')
            assert isinstance(mailids,list)
            assert len(mailids) == 0

    class Tests_get_unread_mailids:
        def test_raises_Exception_if_no_mailbox_open(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            mailreceiver.connect()
            with pytest.raises(Exception):
                mailreceiver.get_unread_mailids()

        def test_returns_list_of_mailids_from_currently_open_mailbox(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            mailreceiver.connect()
            mailreceiver.open_mailbox('Inbox')
            mailids = mailreceiver.get_unread_mailids()
            assert isinstance(mailids,list)
            assert isinstance(mailids[0],bytes)

        def test_returns_list_of_mailids_from_specified_mailbox(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            mailreceiver.connect()
            mailids = mailreceiver.get_unread_mailids('Inbox')
            assert isinstance(mailids,list)
            assert isinstance(mailids[0],bytes)

        def test_returns_empty_list_from_empty_mailbox(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            mailreceiver.connect()
            mailids = mailreceiver.get_unread_mailids('Trash')
            assert isinstance(mailids,list)
            assert len(mailids) == 0

    class Tests_search_for_mailids:
        def test_raises_Exception_if_no_mailbox_open(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            mailreceiver.connect()
            with pytest.raises(Exception):
                mailreceiver.search_for_mailids()

        def test_returns_list_of_mailids_from_currently_open_mailbox(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            mailreceiver.connect()
            mailreceiver.open_mailbox('Inbox')
            mailids = mailreceiver.search_for_mailids('ALL')
            assert isinstance(mailids,list)
            assert isinstance(mailids[0],bytes)

        def test_returns_list_of_mailids_from_specified_mailbox(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            mailreceiver.connect()
            mailids = mailreceiver.search_for_mailids('ALL','Inbox')
            assert isinstance(mailids,list)
            assert isinstance(mailids[0],bytes)

        def test_returns_empty_list_from_empty_mailbox(self):
            mailreceiver = mail.MailReceiver(test_email_settings)
            mailreceiver.connect()
            mailids = mailreceiver.search_for_mailids('ALL','Trash')
            assert isinstance(mailids,list)
            assert len(mailids) == 0

class Tests_MailSender:
    class Tests_init:
        def test_init_raises_Exception_if_no_settings(self):
            with pytest.raises(Exception):
                mailsender = mail.MailSender()

        def test_init_loads_mail_settings(self):
            mailsender = mail.MailSender(test_email_settings)
            assert mailsender._connected == False
            assert mailsender._email_settings is not None
    
    class Tests_connect:
        def test_connect_returns_true_on_connection_success(self):
            mailsender = mail.MailSender(test_email_settings)
            assert mailsender.connect()

    class Tests_disconnect:
        def test_disconnect_returns_true_when_already_disconnected(self):
            mailsender = mail.MailSender(test_email_settings)
            assert mailsender.disconnect()

        def test_disconnect_returns_true_after_disconnecting_from_connected(self):
            mailsender = mail.MailSender(test_email_settings)
            mailsender.connect()
            assert mailsender.disconnect()
