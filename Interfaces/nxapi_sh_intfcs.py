import xlsxwriter
from sys import argv
from datetime import datetime
from functions import nx_login
from nxapi_class import NxIntfc
from collections import OrderedDict


def main(switch):
    """
    This makes an API call to a switch to collect interface stats, and
    then filters the results to just the relevant information. This data
    is then saved to a file named "switchname_date_hourminute.xlsx."

    :param switch: The switch to view interfaces.

    :saves: A xlsx with column headers and their corresponding values
    for each interface on the switch.

    :example:
    (py3) C:\\Users>python nxapi_sh_intfcs.py 10.1.1.1
    What is your username: admin
    What is your password
    (EXAMPLE is 10.1.1.1_14122016_054.xlsx)
    """
    header = nx_login(switch)
    sw_intfcs = NxIntfc(header, switch)
    sh_sw_intfcs = sh_intfcs_fltr(sw_intfcs.sh_intfcs())

    current = datetime.now()
    stamp = '{}{}{}_{}{}'.format(
        current.day, current.month, current.year, current.hour, current.minute
    )

    workbook = xlsxwriter.Workbook('{}_{}.xlsx'.format(switch, stamp))
    worksheet = workbook.add_worksheet()
    format = workbook.add_format({'bold': True})

    column = 0
    row = 0
    for key in sh_sw_intfcs[0]:
        worksheet.write_string(column, row, key, format)
        row += 1

    for entry in sh_sw_intfcs:
        row = 0
        column += 1
        for key in entry:
            worksheet.write(column, row, entry[key])
            row += 1

    worksheet.freeze_panes(1, 0)
    workbook.close()


def sh_intfcs_fltr(req):
    """
    This filters the information returned from the show interfaces request
    to just the relevant information. The nx-api uses different keys, and
    provides different relevant keys based on they type of interface (mgmt,
    ethernet, svi, port-channel). This function first filters to identify
    the type of interface, and each interface is then filtered into an
    identical Ordered Dictionary so that all counters are aligned.

    :param req: The results of an API request for "show interfaces"

    :return: A list of ordered dictionaries corresponding to each interface.
    """
    sh_intfcs_json = req.json()['result']['body']['TABLE_interface']['ROW_interface']

    sh_intfcs_list = []
    for intfc_dict in sh_intfcs_json:
        if "Ethernet" in intfc_dict["interface"]:
            try:
                desc = intfc_dict["desc"]
            except KeyError:
                desc = "blank"

            if intfc_dict["state"] == "down":
                reason = intfc_dict["state_rsn_desc"]
            else:
                reason = 'up'

            try:
                mode = intfc_dict["eth_mode"]
            except KeyError:
                mode = "routed"

            try:
                ip = intfc_dict["eth_ip_addr"]
                mask = intfc_dict["eth_ip_mask"]
            except KeyError:
                ip = "none"
                mask = "none"

            sh_intfcs_list.append(OrderedDict(
                [
                    ("INTERFACE", intfc_dict["interface"]),
                    ("DESCRIPTION", desc),
                    ("TYPE", intfc_dict["eth_hw_desc"]),
                    ("ADMIN", intfc_dict["admin_state"]),
                    ("STATE", intfc_dict["state"]),
                    ("REASON", reason),
                    ("SPEED", intfc_dict["eth_speed"]),
                    ("DUPLEX", intfc_dict["eth_duplex"]),
                    ("NEGOTIATION", intfc_dict["eth_autoneg"]),
                    ("MODE", mode),
                    ("IP", "{}/{}".format(ip, mask)),
                    ("MTU", intfc_dict["eth_mtu"]),
                    ("BWIDTH", intfc_dict["eth_bw"]),
                    ("DELAY", intfc_dict["eth_dly"]),
                    ("TX LOAD", intfc_dict["eth_txload"]),
                    ("RX LOAD", intfc_dict["eth_rxload"]),
                    ("RELIABILITY", intfc_dict["eth_reliability"]),
                    ("LAST FLAP", intfc_dict["eth_link_flapped"]),
                    ("LAST CLEAR", intfc_dict["eth_clear_counters"]),
                    ("LOAD INTERVAL", intfc_dict["eth_load_interval1_rx"]),
                    ("CRC", intfc_dict["eth_crc"]),
                    ("RX ERRORS", intfc_dict["eth_inerr"]),
                    ("RX DISCARDS", intfc_dict["eth_indiscard"]),
                    ("TX ERRORS", intfc_dict["eth_outerr"]),
                    ("TX DISCARDS", intfc_dict["eth_outdiscard"]),
                    ("PC MEMBBERS", "N/A")
                ]
            ))

        elif "Vlan" in intfc_dict["interface"]:
            try:
                desc = intfc_dict["desc"]
            except KeyError:
                desc = "blank"

            if intfc_dict["svi_admin_state"] == "down":
                reason = intfc_dict["svi_rsn_desc"]
            else:
                reason = 'up'

            try:
                ip = intfc_dict["svi_ip_addr"]
                mask = intfc_dict["svi_ip_mask"]
            except KeyError:
                ip = "none"
                mask = "none"

            sh_intfcs_list.append(OrderedDict(
                [
                    ("INTERFACE", intfc_dict["interface"]),
                    ("DESCRIPTION", desc),
                    ("TYPE", "SVI"),
                    ("ADMIN", intfc_dict["svi_admin_state"]),
                    ("STATE", intfc_dict["svi_line_proto"]),
                    ("REASON", reason),
                    ("SPEED", "N/A"),
                    ("DUPLEX", "N/A"),
                    ("NEGOTIATION", "N/A"),
                    ("MODE", "N/A"),
                    ("IP", "{}/{}".format(ip, mask)),
                    ("MTU", intfc_dict["svi_mtu"]),
                    ("BWIDTH", intfc_dict["svi_bw"]),
                    ("DELAY", intfc_dict["svi_delay"]),
                    ("TX LOAD", intfc_dict["svi_tx_load"]),
                    ("RX LOAD", intfc_dict["svi_rx_load"]),
                    ("RELIABILITY", "N/A"),
                    ("LAST FLAP", "N/A"),
                    ("LAST CLEAR", intfc_dict["svi_time_last_cleared"]),
                    ("LOAD INTERVAL", "N/A"),
                    ("CRC", "N/A"),
                    ("RX ERRORS", "N/A"),
                    ("RX DISCARDS", "N/A"),
                    ("TX ERRORS", "N/A"),
                    ("TX DISCARDS", "N/A"),
                    ("PC MEMBBERS", "N/A")
                ]
            ))

        elif "port-channel" in intfc_dict["interface"]:
            try:
                desc = intfc_dict["desc"]
            except KeyError:
                desc = "blank"

            if intfc_dict["state"] == "down":
                reason = intfc_dict["state_rsn_desc"]
            else:
                reason = 'up'

            try:
                ip = intfc_dict["eth_ip_addr"]
                mask = intfc_dict["eth_ip_mask"]
            except KeyError:
                ip = "none"
                mask = "none"

            sh_intfcs_list.append(OrderedDict(
                [
                    ("INTERFACE", intfc_dict["interface"]),
                    ("DESCRIPTION", desc),
                    ("TYPE", intfc_dict["eth_hw_desc"]),
                    ("ADMIN", intfc_dict["admin_state"]),
                    ("STATE", intfc_dict["state"]),
                    ("REASON", reason),
                    ("SPEED", intfc_dict["eth_speed"]),
                    ("DUPLEX", intfc_dict["eth_duplex"]),
                    ("NEGOTIATION", "N/A"),
                    ("MODE", "N/A"),
                    ("IP", "{}/{}".format(ip, mask)),
                    ("MTU", intfc_dict["eth_mtu"]),
                    ("BWIDTH", intfc_dict["eth_bw"]),
                    ("DELAY", intfc_dict["eth_dly"]),
                    ("TX LOAD", intfc_dict["eth_txload"]),
                    ("RX LOAD", intfc_dict["eth_rxload"]),
                    ("RELIABILITY", intfc_dict["eth_reliability"]),
                    ("LAST FLAP", "N/A"),
                    ("LAST CLEAR", intfc_dict["eth_clear_counters"]),
                    ("LOAD INTERVAL", intfc_dict["eth_load_interval1_rx"]),
                    ("CRC", intfc_dict["eth_crc"]),
                    ("RX ERRORS", intfc_dict["eth_inerr"]),
                    ("RX DISCARDS", intfc_dict["eth_indiscard"]),
                    ("TX ERRORS", intfc_dict["eth_outerr"]),
                    ("TX DISCARDS", intfc_dict["eth_outdiscard"]),
                    ("PC MEMBBERS", intfc_dict["eth_members"])
                ]
            ))

        elif "mgmt" in intfc_dict["interface"]:
            try:
                desc = intfc_dict["desc"]
            except KeyError:
                desc = "blank"

            if intfc_dict["state"] == "down":
                reason = intfc_dict["state_rsn_desc"]
            else:
                reason = 'up'

            try:
                mode = intfc_dict["eth_mode"]
            except KeyError:
                mode = "routed"

            try:
                ip = intfc_dict["eth_ip_addr"]
                mask = intfc_dict["eth_ip_mask"]
            except KeyError:
                ip = "none"
                mask = "none"

            sh_intfcs_list.append(OrderedDict(
                [
                    ("INTERFACE", intfc_dict["interface"]),
                    ("DESCRIPTION", desc),
                    ("TYPE", intfc_dict["eth_hw_desc"]),
                    ("ADMIN", intfc_dict["admin_state"]),
                    ("STATE", intfc_dict["state"]),
                    ("REASON", reason),
                    ("SPEED", intfc_dict["eth_speed"]),
                    ("DUPLEX", intfc_dict["eth_duplex"]),
                    ("NEGOTIATION", intfc_dict["eth_autoneg"]),
                    ("MODE", mode),
                    ("IP", "{}/{}".format(ip, mask)),
                    ("MTU", intfc_dict["eth_mtu"]),
                    ("BWIDTH", intfc_dict["eth_bw"]),
                    ("DELAY", intfc_dict["eth_dly"]),
                    ("TX LOAD", intfc_dict["eth_txload"]),
                    ("RX LOAD", intfc_dict["eth_rxload"]),
                    ("RELIABILITY", intfc_dict["eth_reliability"]),
                    ("LAST FLAP", "N/A"),
                    ("LAST CLEAR", "N/A)"),
                    ("LOAD INTERVAL", "N/A"),
                    ("CRC", "N/A"),
                    ("RX ERRORS", "N/A"),
                    ("RX DISCARDS", "N/A"),
                    ("TX ERRORS", "N/A"),
                    ("TX DISCARDS", "N/A"),
                    ("PC MEMBBERS", "N/A")
                ]
            ))

        else:
            pass

    return sh_intfcs_list


if __name__ == '__main__':
    main(argv[1])
