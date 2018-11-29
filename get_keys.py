import os
import sys
import ConfigParser
from gnome_connection_manager import conf, HostUtils

def load_encryption_key():
    global enc_passwd
    try:
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE) as f:
                enc_passwd = f.read()
        else:
            enc_passwd = ''
    except:
        print("Error trying to open key_file")
        enc_passwd = ''

def get_username():
    return os.getenv('USER') or os.getenv('LOGNAME') or os.getenv('USERNAME')

def get_password():
    return get_username() + enc_passwd

HOME = os.path.join(os.getenv("HOME"), ".gcm")
if len(sys.argv) > 1:
    HOME = sys.argv[1]
print(HOME)
CONFIG_FILE = os.path.join(HOME, "gcm.conf")
KEY_FILE = os.path.join(HOME, ".gcm.key")
print(CONFIG_FILE, KEY_FILE)

load_encryption_key()

cp = ConfigParser.RawConfigParser()
cp.read(CONFIG_FILE)

conf.VERSION = cp.get("options", "version")
passwd = get_password()

# Leer lista de hosts
groups = {}
for section in cp.sections():
    if not section.startswith("host "):
        continue
    host = cp.options(section)
    try:
        host = HostUtils.load_host_from_ini(cp, section, passwd)

        if host.group not in groups:
            groups[host.group] = []

        groups[host.group].append(host)
    except:
        print "%s: %s" % ("Invalid entry in config file", sys.exc_info()[1])

for g in groups:
    print(g)
    for h in groups[g]:
        print(h.name, h.type, h.host, h.port, h.user, h.password, h.private_key)
