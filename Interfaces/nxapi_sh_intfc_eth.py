from sys import argv
from nxapi_class import NxIntfc
from functions import nx_login, http_check


def main(switch, intfc):
    """
    This function is used to print out the relevant "show
    interface" data for a specific ethernet interface.

    :param switch: The switch to view interface stats.
    :param intfc: The interface of interest.

    :prints: The relevant show interface data.

    :example:
    (py3) C:\\Users>python nxapi_sh_intfc.py 10.1.1.1 eth1/48
    What is your username: admin
    What is your password
    Eth1/48
      admin up, state up, up
      member of Po1000
      type 1000/10000 Ethernet, media 10G
      speed 10 Gb/s, duplex full
      mtu 1500, bw 10000000
      rx 1 of 255
      tx 1 of 255
      mode trunk
      last flapped 3d18h, last cleared 3d19h
      0 crc
      0 collisions
      0 rx errors, 0 tx errors
    """
    header = nx_login(switch)
    sw_intfc = NxIntfc(header, switch, intfc)
    sh_sw_intfc = sw_intfc.sh_intfc()

    http_check(sh_sw_intfc)
    sh_sw_intfc_filtr = intfc_eth_filtr(sh_sw_intfc)

    print("{}\n  admin {}, state {}, {}\n  member of {}\
          \n  type {}, media {}\n  speed {}, duplex {}\
          \n  mtu {}, bw {}\n  rx {} of 255\n  tx {} of 255\
          \n  mode {}\n  last flapped {}, last cleared {}\
          \n  {} crc\n  {} collisions\n  {} rx errors, {} tx errors"
          "\n".format(intfc, sh_sw_intfc_filtr["admin"], sh_sw_intfc_filtr["state"],
                      sh_sw_intfc_filtr["reason"], sh_sw_intfc_filtr["bundle"],
                      sh_sw_intfc_filtr["type"], sh_sw_intfc_filtr["media"],
                      sh_sw_intfc_filtr["speed"], sh_sw_intfc_filtr["duplex"],
                      sh_sw_intfc_filtr["mtu"], sh_sw_intfc_filtr["bw"],
                      sh_sw_intfc_filtr["rx_load"], sh_sw_intfc_filtr["tx_load"],
                      sh_sw_intfc_filtr["mode"], sh_sw_intfc_filtr["flapped"],
                      sh_sw_intfc_filtr["cleared"], sh_sw_intfc_filtr["crc"],
                      sh_sw_intfc_filtr["collision"], sh_sw_intfc_filtr["rx_err"],
                      sh_sw_intfc_filtr["tx_err"]))


def intfc_eth_filtr(req):
    """
    This filters the information returned from the show interface request
    to just the relevant information. The nx-api uses different keys, and
    provides different relevant keys based on they type of interface (mgmt,
    ethernet, svi, port-channel). This function filters specifically for
    ethernet interfaces. Some dictionary keys are only returned under
    certain conditions, therefor test are done before adding to the final
    dictionary.

    :param req: The results of an API request for "show interface"

    :return: A dictionary of interesting fields from "show interface eth x/y".
    """
    sh_sw_intfc_json = req.json()['result']['body']['TABLE_interface']['ROW_interface']

    if sh_sw_intfc_json["state"] != "up":
        reason = sh_sw_intfc_json["state_rsn_desc"]
    else:
        reason = 'up'

    try:
        bundle = sh_sw_intfc_json["eth_bundle"]
    except KeyError:
        bundle = "Not Bundled"

    try:
        media = sh_sw_intfc_json["eth_media"]
    except:
        media = "None"

    return {
        "admin": sh_sw_intfc_json["admin_state"],
        "state": sh_sw_intfc_json["state"],
        "reason": reason,
        "bundle": bundle,
        "type": sh_sw_intfc_json["eth_hw_desc"],
        "mtu": sh_sw_intfc_json["eth_mtu"],
        "bw": sh_sw_intfc_json["eth_bw"],
        "rx_load": sh_sw_intfc_json["eth_rxload"],
        "tx_load": sh_sw_intfc_json["eth_txload"],
        "mode": sh_sw_intfc_json["eth_mode"],
        "speed": sh_sw_intfc_json["eth_speed"],
        "duplex": sh_sw_intfc_json["eth_duplex"],
        "media": media,
        "flapped": sh_sw_intfc_json["eth_link_flapped"],
        "cleared": sh_sw_intfc_json["eth_clear_counters"],
        "crc": sh_sw_intfc_json["eth_crc"],
        "rx_err": sh_sw_intfc_json["eth_inerr"],
        "tx_err": sh_sw_intfc_json["eth_outerr"],
        "collision": sh_sw_intfc_json["eth_coll"]
    }


if __name__ == '__main__':
    main(argv[1], argv[2])
