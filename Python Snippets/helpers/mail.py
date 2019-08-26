import logging, os, sys
import email
import imaplib
import json
import smtplib
import unicodedata

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from helpers import file
from helpers import regex
from helpers import path

class MailReceiver():
    def __init__(self,settings_file):
        if settings_file is None:
            raise Exception('Missing required settings.json file')
        self._connected = False
        self._mailboxopen = False
        self.downloadoptions = self.DownloadOptions(self)
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__,settings_file)) as json_file:
            self._emailsettings = json.load(json_file)
        return

    def __del__(self):
        self.disconnect(refresh=False)
        return

    def connect(self):
        if not self._connected:
            resp, data = self.imapconn.login(self._emailsettings['Username'], self._emailsettings['Password'])
            if resp == 'OK':
                self._connected = True
        return self._connected

    def disconnect(self,refresh=True):
        if self._mailboxopen:
            self.close_mailbox()
        if self._connected:
            resp, data = self.imapconn.logout()
            if resp == 'BYE':
                self._connected = False
                if refresh:
                    self._setup_connection_type()
        return not self._connected

    def open_mailbox(self,mailbox):
        if self._mailboxopen:
            self.close_mailbox()
        resp, data = self.imapconn.select(mailbox)
        if resp == 'OK':
            self._mailboxopen = True
        return self._mailboxopen

    def close_mailbox(self):
        if self._mailboxopen:
            resp, data = self.imapconn.close()
            if resp == 'OK':
                self._mailboxopen = False
        return not self._mailboxopen

    def retrieve_mail_message(self,mailid):
        return retrieve_mail_messages([mailid])[0]

    def retrieve_mail_messages(self,mailids):
        if not self._mailboxopen:
            raise Exception(r'No mailbox currently open')
        msgs = []
        for mailid in mailids:
            resp, data = self.imapconn.fetch(mailid, "(RFC822)")
            if resp == 'OK':
                msgs.append(email.message_from_bytes(data[0][1]))
            else:
                msgs.append(None)
        return msgs

    def move_mail_message(self,mailid,to_mailbox):
        return move_mail_messages([mailid],to_mailbox)[0]

    def move_mail_messages(self,mailids,to_mailbox):
        if not self._mailboxopen:
            raise Exception(r'No mailbox currently open')
        success = []
        for mailid in mailids:
            resp, data = self.imapconn.copy(mailid,to_mailbox)
            resp, data = self.imapconn.store(mailid, '+FLAGS', r'(\Deleted)')
            success.append(True) if resp == 'OK' else success.append(False)
        resp, data = self.imapconn.expunge()
        return success

    def delete_mail_message(self,mailid):
        return delete_mail_messages([mailid])[0]

    def delete_mail_messages(self,mailids):
        if not self._mailboxopen:
            raise Exception(r'No mailbox currently open')
        success = []
        for mailid in mailids:
            resp, data = self.imapconn.store(mailid, '+FLAGS', r'(\Deleted)')
            success.append(True) if resp == 'OK' else success.append(False)
        resp, data = self.imapconn.expunge()
        return success

    def get_all_mailids(self,mailbox):
        mailids = search_for_mailids(mailbox,r'ALL')
        return mailids

    def get_unread_mailids(self,mailbox):
        mailids = search_for_mailids(mailbox,r'UNSEEN')
        return mailids

    def search_for_mailids(self,mailbox,searchby):
        self.open_mailbox(mailbox)
        resp, data = self.imapconn.search(None,searchby)
        if resp == 'OK':
            mailids = data[0].split()
        return mailids

    def _setup_connection_type(self):
        if self._emailsettings['IMAP Settings']['SSL']:
            self.imapconn = imaplib.IMAP4_SSL(self._emailsettings['IMAP Settings']['Host'],self._emailsettings['IMAP Settings']['Port'])
        return True

    def download_mail_attachments(self,msg,download_folder):
        attachments = []
        attachment_parts = MailReceiver.GetAttachmentParts(msg)
        for attachment in attachment_parts:
            filename = regex.illegal_basefilename_chars.sub(attachment.get_filename().lower(),'')
            file_ext = os.path.splitext(filename)[1].lower()
            if (self.downloadoptions.filter_by_extension is None) or \
               (file_ext in self.downloadoptions.filter_by_extension):
                download_filename = path.combine(download_folder,filename)
                download_filename = file._incrementfilename(download_filename)
                attachments.append(MailReceiver._save_attachment_part(attachment,download_filename))
        return attachments

    @staticmethod
    def _retrieve_attachment_parts(msg):
        attachment_parts = []
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            if part.get_filename() is not None:
                attachment_parts.append(part)
        return attachment_parts

    @staticmethod
    def _save_attachment_part(attachment_part,download_filename):
        with open(download_filename, 'wb') as fout:
            fout.write(attachment_part.get_payload(decode=True))
        return download_filename

    @staticmethod
    def _retrieve_attachment_filesize(attachment_part):
        filesize = 0
        return filesize

    class DownloadOptions():
        def __init__(self,mailreceiver):
            self._mailreceiver = mailreceiver
            self.filter_by_extension = []
            self.filter_by_size_kb = None

class MailSender():
    def __init__(self,settings_file):
        if settings_file is None:
            raise Exception('Missing required settings.json file')
        self._connected = False
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__,settings_file)) as json_file:
            self._emailsettings = json.load(json_file)
        return
    
    def __del__(self):
        self.disconnect()
        return

    def connect(self):
        if not self._connected:
            self._setup_connection_type()
            if self._emailsettings['SMTP Settings']['TLS']:
                self.smtpconn.starttls()
            resp = self.smtpconn.login(self._emailsettings['Username'],self._emailsettings['Password'])
            if ('Authentication successful' in str(resp[1])):
                self._connected = True
        return self._connected

    def disconnect(self):
        if self._connected:
            resp = self.smtpconn.quit()
            if ('Service closing transmission channel' in str(resp[1])):
                self._connected = False
        return not self._connected

    def send_mail_message(self,msg):
        self.send_mail_messages([msg])
        return True

    def send_mail_messages(self,msgs):
        if self.connect():
            for msg in msgs:
                self.smtpconn.send_message(msg)
        self.disconnect(refresh=True)
        return True

    def create_new_plantext_message(self,mailto,subject,bodytext,attachements=[]):
        msg = self._create_mail_header(self._emailsettings['Username'],mailto,subject)
        msg.attach(MIMEText(bodytext, "plain"))
        msg = MailSender._attach_files(msg,attachements)
        return msg

    def create_new_html_message(self,mailto,subject,bodyhtml,attachements=[]):
        msg = self._create_mail_header(self._emailsettings['Username'],mailto,subject)
        msg.attach(MIMEText(bodyhtml, "html"))
        msg = MailSender._attach_files(msg,attachements)
        return msg

    def _setup_connection_type(self):
        if self._emailsettings['SMTP Settings']['TLS']:
            self.smtpconn = smtplib.SMTP(self._emailsettings['SMTP Settings']['Host'],self._emailsettings['SMTP Settings']['Port'])
        if self._emailsettings['SMTP Settings']['SSL']:
            self.smtpconn = smtplib.SMTP_SSL(self._emailsettings['SMTP Settings']['Host'],self._emailsettings['SMTP Settings']['Port'])
        return True

    @staticmethod
    def _create_mail_header(self,mailfrom,mailto,subject):
        msg = MIMEMultipart()
        msg["From"] = mailfrom
        msg["To"] = mailto
        msg["Subject"] = subject
        return msg

    @staticmethod
    def _attach_files(msg,attachments=[]):
        for filename in attachments:
            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition","attachment; filename="+os.path.basename(filename))
                msg.attach(part)
        return msg