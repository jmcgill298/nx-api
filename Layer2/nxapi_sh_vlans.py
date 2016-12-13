from sys import argv
from functions import nx_login
from nxapi_class import NxL2


def main(switch):
    """
    :param switch: The switch to view VLAN information.

    :prints: The VLAN information for the switch, or the reason for http failure.

    :example:
    (py3) C:\\Users>python nxapi_sh_vlans.py 10.1.1.1
    What is your username: admin
    What is your password

    VLAN: 1
      Name: default
      Ethernet1/1,Ethernet1/2,Ethernet1/3,Ethernet1/4,Ethernet1/5,Ethernet1/6,Ethernet1/7,
      Ethernet1/8,Ethernet1/9,Ethernet1/10,Ethernet1/11,Ethernet1/12,Ethernet1/13
      Ethernet1/14,Ethernet1/15,Ethernet1/16,Ethernet1/17,Ethernet1/18,Ethernet1/19,
      Ethernet1/20,Ethernet1/21,Ethernet1/22,Ethernet1/23,Ethernet1/24,Ethernet1/25,
      Ethernet1/26,Ethernet1/27,Ethernet1/28,Ethernet1/29,Ethernet1/30,Ethernet1/31,
      Ethernet1/32,Ethernet1/33,Ethernet1/34,Ethernet1/35,Ethernet1/36,Ethernet1/37,
      Ethernet1/38,Ethernet1/39,Ethernet1/40,Ethernet1/41,Ethernet1/42,Ethernet1/43,
      Ethernet1/44,Ethernet1/46,Ethernet1/48,Ethernet2/1,Ethernet2/2,Ethernet2/3,
      Ethernet2/4,Ethernet2/5,Ethernet2/6,Ethernet2/7,Ethernet2/8,Ethernet2/9,Ethernet2/10,
      Ethernet2/11,Ethernet2/12


    VLAN: 10
      Name: web
      Ethernet1/45,Ethernet1/47


    VLAN: 20
      Name: database
      None
    """
    header = nx_login(switch)

    sw_vlans = NxL2(header, switch)
    sh_vlans = sw_vlans.sh_vlan()
    if sh_vlans.ok:
        sh_vlans_dict = vlans_fltr(sh_vlans)
        for vlan in sh_vlans_dict:
            print("\nVLAN: {}\n  Name: {}\n  {}\n".format(
                vlan["vlan_id"], vlan["name"], vlan["interfaces"]
            ))
    else:
        print('HTTP REQUEST FAILED:\nStatus Code: {}\nReason: {}\nContent: {}'.format(
            sh_vlans.status_code, sh_vlans.reason, sh_vlans.content))


def vlans_fltr(req):
    """
    This filters the information returned from the VLAN request to just the
    relevant information (VLAN ID, VLAN Name, and interfaces associated
    with the VLAN). Try and except are used for the interfaces, as the
    dictionary key will not exist if no interfaces belong to the VLAN,
    which will then raise an error.

    :param req: The results of an API request for "show vlans"

    :return: A list of dictionaries for each VLAN consisting of ID,
    Name, and associated interfaces.
    """
    sw_vlans_json = req.json()["result"]["body"]["TABLE_vlanbrief"]["ROW_vlanbrief"]

    sw_vlans_list = []
    for vlan in sw_vlans_json:
        vlan_id = vlan["vlanshowbr-vlanid"]
        vlan_name = vlan["vlanshowbr-vlanname"]
        try:
            vlan_int = vlan["vlanshowplist-ifidx"]
        except:
            vlan_int = "None"

        sw_vlans_list.append({
            "vlan_id": vlan_id,
            "name": vlan_name,
            "interfaces": vlan_int
        })

    return sw_vlans_list


if __name__ == '__main__':
    main(argv[1])
