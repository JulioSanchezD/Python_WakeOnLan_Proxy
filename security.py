import json, smtplib, ssl, os

port = 465 # For SSL

# Create a secure SSL context
context = ssl.create_default_context()

with open("config.json") as config_file:
	config = json.load(config_file)

MAC_ADDRESS = config.get('MAC_ADDRESS')
MAIL = config.get('MAIL')
PASSWORD = config.get('PASSWORD')

def email(data, mac=None):
	os.system("sudo ufw allow 443/tcp")
	os.system("sudo ufw --force enable")
	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
		server.login(MAIL, PASSWORD)
		if mac:
			message = """\
Someone tried to wake up an unknown computer. Closing port 9..."""
		else:
			message = """\
Unknown packet entered port 9, closing port..."""
		server.sendmail(MAIL, MAIL, message)
	os.system("sudo ufw delete allow 443/tcp")
	os.system("sudo ufw --force enable")

def verify(data):
        if len(data) == 102:
            try:
                sync = data[0:6].hex()
                content = data[6:].hex()
            except:
                email(data)
                return False
            else:
                for i in range(0, 16):
                    mac = content[12*i:12*i+12]
                    if mac != MAC_ADDRESS:
                        email(data, mac)
                        return False
                return True
        email(data)
        return False
