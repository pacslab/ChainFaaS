import configparser

import os
import sys
import subprocess

if os.geteuid() == 0:
    print("We're root!")
    PATH = r'/etc/MSc_Research_Django/settings.ini'
    config = configparser.RawConfigParser()
    # config.read(PATH)

    # config.set('fabric', 'CONTROLLER_TOKEN', 'Haha!')

    # with open('/etc/MSc_Research_Django/settings.ini', 'r+') as configfile:
    #     # configfile.write('Hey!')
    # print(configfile.read())
    config.read(PATH)
    print(config.get('fabric', 'CONTROLLER_TOKEN'))
    config.set('fabric', 'CONTROLLER_TOKEN', 'Woooww!!')

    with open(PATH, 'w') as configfile:
        config.write(configfile)
else:
    print("We're not root.")
    subprocess.call(['sudo', 'python3', *sys.argv])
    sys.exit()

