from sys import argv
from nxapi_class import NxL2
from functions import nx_login


def main(switch, name, vlan):
    """
    :param switch: The switch to configure the new VLAN.
    :param name: The name or description of the VLAN.
    :param vlan: The VLAN to configure.

    :prints: The results of the configuration request.

    :example:
    (py3) C:\\Users>python nxapi_conf_vlan.py 10.1.1.1 private 30
    What is your username: admin
    What is your password
    VLAN 30 was created with the name, private, on 10.1.1.1
    """
    header = nx_login(switch)
    sw_vlan = NxL2(header, switch, vlan)
    vlan_conf = sw_vlan.conf_vlan(name, vlan)

    if vlan_conf.ok:
        print("VLAN {} was created with the name {}"
              " on {}".format(vlan, name, switch))
    else:
        ('HTTP REQUEST FAILED:\nStatus Code: {}\nReason: {}\nContent: {}'.format(
            vlan_conf.status_code, vlan_conf.reason, vlan_conf.content))


if __name__ == '__main__':
    main(argv[1], argv[2],argv[3])
    
