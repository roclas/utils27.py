# Something in lines of http://stackoverflow.com/questions/348630/how-can-i-download-all-emails-with-attachments-from-gmail
# Make sure you have IMAP enabled in your gmail settings.
# Right now it won't download same file name twice even if their contents are different.

import gmail_credentials 
import email
import getpass, imaplib
import os
import sys
import re
 
detach_dir = '.'
if 'attachments' not in os.listdir(detach_dir):
    os.mkdir('attachments')
 
userName = gmail_credentials.email
passwd = gmail_credentials.password
 
try:
    imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
    typ, accountDetails = imapSession.login(userName, passwd)
    if typ != 'OK':
        print 'Not able to sign in!'
        raise
    
    #imapSession.select('[Gmail]/All Mail')
    imapSession.select('INBOX')
    #typ, data = imapSession.search(None, 'ALL')
    #typ, data = imapSession.search(None, 'UNSEEN')
    typ, data = imapSession.search(None, '(UNSEEN SUBJECT "%s")' % u"download-me".encode("utf-8"))
    if typ != 'OK':
        print 'Error searching Inbox.'
        raise
    
    # Iterating over all emails
    for msgId in data[0].split():
        typ,messageParts=imapSession.fetch(msgId,'(RFC822)')
        if typ != 'OK':
            print 'Error fetching mail.'
            raise
        tuples= messageParts[0]
        emailBody = tuples[1]
        mail = email.message_from_string(emailBody)
        for part in mail.walk():
	    """
	    try:
	     subj=[v for (k,v) in 
		part._headers if k.lower()=="subject"][0]
	    except:
		pass
	    """
            if part.get_content_maintype() == 'multipart':
                # print part.as_string()
                continue
            if part.get('Content-Disposition') is None:
                # print part.as_string()
                continue
            fileName = part.get_filename()
 
            if bool(fileName):
                filePath = os.path.join(detach_dir, 'attachments', fileName)
                if not os.path.isfile(filePath) :
                    print fileName
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
    imapSession.close()
    imapSession.logout()
except :
    print 'Not able to download all attachments.'
