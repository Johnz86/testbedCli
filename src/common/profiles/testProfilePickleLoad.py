import os
import ConfigParser
import collections
import json
from pprint import pprint

 #   INSTAL_SERVER = INS;
 #   ADMINISTRATOR = ADM;
 #   DIRECTORY_SERVER = NDS;
 #   PROVISIONING_GATEWAY = PGW;
 #   SYSTEM_MONITOR = SIM;

INSTAL_SERVER = 1;
ADMINISTRATOR = 2;
DIRECTORY_SERVER = 3;
PROVISIONING_GATEWAY = 4;
SYSTEM_MONITOR = 5;

NODE_TYPE = {
    INSTAL_SERVER: 'INS',
    ADMINISTRATOR: 'ADM',
    DIRECTORY_SERVER: 'NDS',
    PROVISIONING_GATEWAY:'PGW',
    SYSTEM_MONITOR: 'SIM'
}

print NODE_TYPE.viewvalues()
print NODE_TYPE.keys(), NODE_TYPE.items(), NODE_TYPE.viewitems(), NODE_TYPE.viewkeys(), NODE_TYPE[SYSTEM_MONITOR], NODE_TYPE.items()

filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'janci_V9_SP2.txt')
config = ConfigParser.ConfigParser()
config.read(filePath)
result = []
#print type(config._sections)
con = collections.OrderedDict(config._sections)
#pprint(con);
#for key, car in con.items():
#    print(key)
#    for attribute, value in car.items():
#        print('{} : {}'.format(attribute, value))

obj = {"profile":"path", "profileData": con}
obj2 = {"profile":"path2", "profileData": con}
result.append(obj)
result.append(obj2)

#print json.dumps(result)