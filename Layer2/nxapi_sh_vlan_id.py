from sys import argv
from functions import nx_login
from nxapi_class import NxL2


def main(switch, vlan):
    """
    :param switch: The switch to view VLAN information.
    :param vlan: The VLAN to view.

    :prints: The information for the VLAN, or the reason for http failure.

    :example:
    (py3) C:\\Users>python nxapi_sh_vlans.py 10.1.1.1 10
    What is your username: admin
    What is your password

    VLAN: 10
      Name: web
      Ethernet1/45,Ethernet1/47

    """
    header = nx_login(switch)

    sw_vlan = NxL2(header, switch)
    sh_vlan = sw_vlan.sh_vlan_id(vlan)
    if sh_vlan.ok:
        sh_vlan_dict = vlan_fltr(sh_vlan, vlan)
        print("\nVLAN: {}\n  Name: {}\n  {}\n".format(
            vlan, sh_vlan_dict["name"], sh_vlan_dict["interfaces"]
        ))
    else:
        print('HTTP REQUEST FAILED:\nStatus Code: {}\nReason: {}\nContent: {}'.format(
            sh_vlan.status_code, sh_vlan.reason, sh_vlan.content))


def vlan_fltr(req, vlan):
    """
    This filters the information returned from the VLAN request to just the
    relevant information (VLAN ID, VLAN Name, and interfaces associated
    with the VLAN). Try and except are used for the conversion to json and
    the interfaces extraction, as the dictionary keys will not exist if they
    do not have values, which will then raise an error.

    :param req: The results of an API request for "show vlan id #"

    :return: A dictionary for VLAN consisting of Name, and associated interfaces.
    """
    try:
        sw_vlan_json = req.json()["result"]["body"]["TABLE_vlanbriefid"]["ROW_vlanbriefid"]
    except TypeError:
        print("\nVLAN {} DOES NOT EXIST".format(vlan))
        exit(1)

    vlan_name = sw_vlan_json["vlanshowbr-vlanname"]
    try:
        vlan_int = sw_vlan_json["vlanshowplist-ifidx"]
    except KeyError:
        vlan_int = "None"

    return {
        "name": vlan_name,
        "interfaces": vlan_int
    }


if __name__ == '__main__':
    main(argv[1], argv[2])
