import logging, os, sys
import email
import imaplib
import json
import numpy
import smtplib
import unicodedata

from datetime import datetime
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
            raise Exception('No settings.json file')
        self._connected = False
        self._mailboxopen = None
        self.download_options = self.DownloadOptions(self)
        with open(settings_file) as json_file:
            self._email_settings = json.load(json_file)
        return

    def connect(self):
        if not self._connected:
            self._setup_connection_type()
            resp, data = self.imapconn.login(self._email_settings['Username'], self._email_settings['Password'])
            if resp == 'OK':
                self._connected = True
        return self._connected

    def disconnect(self):
        if self._mailboxopen:
            self.close_mailbox()
        if self._connected:
            resp, data = self.imapconn.logout()
            if resp == 'BYE':
                self._connected = False
        return not self._connected

    def open_mailbox(self,mailbox='Inbox'):
        if not self._connected:
            self.connect()
        if mailbox != self._mailboxopen:
            self.close_mailbox()
        resp, data = self.imapconn.select(mailbox)
        if resp == 'OK':
            self._mailboxopen = mailbox
        return bool(self._mailboxopen)

    def close_mailbox(self):
        if self._mailboxopen:
            resp, data = self.imapconn.close()
            if resp == 'OK':
                self._mailboxopen = None
        return not self._mailboxopen

    def retrieve_mail_message(self,mailid,markasread=True):
        return self.retrieve_mail_messages([mailid],markasread)[0]

    def retrieve_mail_messages(self,mailids,markasread=True):
        if not self._mailboxopen:
            raise Exception(r'No mailbox currently open')
        msgs = []
        for mailid in mailids:
            if markasread:
                resp, data = self.imapconn.fetch(mailid, "(RFC822)")
            else:
                resp, data = self.imapconn.fetch(mailid, "BODY.PEEK[]")
            if resp == 'OK':
                msgs.append(email.message_from_bytes(data[0][1]))
            else:
                msgs.append(None)
        return msgs

    def move_mail_message(self,mailid,to_mailbox):
        return self.move_mail_messages([mailid],to_mailbox)[0]

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
        return self.delete_mail_messages([mailid])[0]

    def delete_mail_messages(self,mailids):
        if not self._mailboxopen:
            raise Exception(r'No mailbox currently open')
        success = []
        for mailid in mailids:
            resp, data = self.imapconn.store(mailid, '+FLAGS', r'(\Deleted)')
            success.append(True) if resp == 'OK' else success.append(False)
        resp, data = self.imapconn.expunge()
        return success

    def get_all_mailids(self,mailbox=None):
        mailids = self.search_for_mailids(r'ALL',mailbox)
        return mailids

    def get_unread_mailids(self,mailbox=None):
        mailids = self.search_for_mailids(r'UNSEEN',mailbox)
        return mailids

    def search_for_mailids(self,searchby,mailbox=None):
        if mailbox is None:
            if not self._mailboxopen:
                raise Exception(r'No mailbox currently open')
        else:
            self.open_mailbox(mailbox)
        resp, data = self.imapconn.search(None,searchby)
        if resp == 'OK':
            mailids = data[0].split()
        return mailids

    def download_mail_attachments(self,msg,download_folder):
        attachments = []
        attachment_parts = MailReceiver._retrieve_attachment_parts(msg)
        for attachment in attachment_parts:
            filename = regex.illegal_basefilename_chars.sub('',attachment.get_filename().lower())
            file_ext = os.path.splitext(filename)[1].lower()
            if (len(self.download_options.filter_by_extension) == 0) or \
               (file_ext in self.download_options.filter_by_extension):
                download_filename = path.combine(download_folder,filename)
                download_filename = file._increment_filename(download_filename)
                attachment_bytes = MailReceiver._decode_attachment(attachment)
                if MailReceiver._retrieve_attachment_bytes_filesize(attachment_bytes) >= self.download_options.greater_than_size_kb:
                    attachments.append(MailReceiver._save_attachment_bytes(attachment_bytes,download_filename))
        return attachments

    def _setup_connection_type(self):
        if self._email_settings['IMAP Settings']['SSL']:
            self.imapconn = imaplib.IMAP4_SSL(self._email_settings['IMAP Settings']['Host'],self._email_settings['IMAP Settings']['Port'])
        return True

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
        attachment_bytes = MailReceiver._decode_attachment(attachment_part)
        return _save_attachment_bytes(attachment_bytes,download_filename)

    @staticmethod
    def _save_attachment_bytes(attachment_bytes,download_filename):
        file.write_all_bytes(attachment_bytes,download_filename)
        return download_filename

    @staticmethod
    def _retrieve_attachement_filesize(attachment_part):
        attachment_bytes = MailReceiver._decode_attachment(attachment_part)
        return MailReceiver._retrieve_attachment_bytes_filesize(attachment_bytes)

    @staticmethod
    def _retrieve_attachment_bytes_filesize(attachment_bytes):
        return int(numpy.ceil(len(attachment_bytes)/1024))

    @staticmethod
    def _decode_attachment(attachment_part):
        return attachment_part.get_payload(decode=True)

    class DownloadOptions():
        def __init__(self,mailreceiver):
            self._mailreceiver = mailreceiver
            self.filter_by_extension = []
            self.greater_than_size_kb = 0

class MailSender():
    def __init__(self,settings_file):
        if settings_file is None:
            raise Exception('Missing required settings.json file')
        self._connected = False
        with open(settings_file) as json_file:
            self._email_settings = json.load(json_file)
        return

    def connect(self):
        if not self._connected:
            self._setup_connection_type()
            if self._email_settings['SMTP Settings']['TLS']:
                self.smtpconn.starttls()
            resp = self.smtpconn.login(self._email_settings['Username'],self._email_settings['Password'])
            if ('authenticated' in str(resp[1])):
                self._connected = True
        return self._connected

    def disconnect(self):
        if self._connected:
            resp = self.smtpconn.quit()
            if ('goodbye' in str(resp[1])):
                self._connected = False
        return not self._connected

    def send_mail_message(self,msg):
        return self.send_mail_messages([msg])

    def send_mail_messages(self,msgs):
        if self.connect():
            for msg in msgs:
                self.smtpconn.send_message(msg)
        return self.disconnect()

    def create_new_plantext_message(self,mailto,subject,bodytext,attachements=[]):
        msg = self._create_mail_header(self._email_settings['Username'],mailto,subject)
        msg.attach(MIMEText(bodytext, "plain"))
        msg = MailSender._attach_files(msg,attachements)
        return msg

    def create_new_html_message(self,mailto,subject,bodyhtml,attachements=[]):
        msg = MailSender._create_mail_header(self._email_settings['Username'],mailto,subject)
        msg.attach(MIMEText(bodyhtml, "html"))
        msg = MailSender._attach_files(msg,attachements)
        return msg

    def _setup_connection_type(self):
        if self._email_settings['SMTP Settings']['TLS']:
            self.smtpconn = smtplib.SMTP(self._email_settings['SMTP Settings']['Host'],self._email_settings['SMTP Settings']['Port'])
        if self._email_settings['SMTP Settings']['SSL']:
            self.smtpconn = smtplib.SMTP_SSL(self._email_settings['SMTP Settings']['Host'],self._email_settings['SMTP Settings']['Port'])
        return True

    @staticmethod
    def _create_mail_header(mailfrom,mailto,subject):
        msg = MIMEMultipart()
        msg["From"] = mailfrom
        msg["To"] = ','.join(mailto)
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
