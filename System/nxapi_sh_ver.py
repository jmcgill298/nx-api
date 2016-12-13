from sys import argv
from functions import nx_login
from nxapi_class import NxAaa, NxSystem


def main(switch):
    """
    This program is used to print a switches version information.

    :param switch: The switch to issue a "show version" command.

    :prints: The switches version information, or reason for http failure.

    :example:
    (py3) C:\\Users>python nxapi_sh_ver.py '10.1.1.1'
     What is your username: admin
     What is your password

       Hostname: switch1
       Model: Nexus9000 C9396PX Chassis
       OS: 7.0(3)I5(1)
       Uptime: 0 years, 0 months, 20 days, 16 hours, 7 minutes, 31 seconds
       Reload Reason: Power Down/UP epld upgrade process
    """
    header = nx_login(switch)

    sw = NxSystem(header, switch)
    sw_ver = sw.nx_sh_ver()

    if sw_ver.ok:
        ver_dict = sh_ver_filter(sw_ver)
        print("\n Hostname: {}\n Model: {}\n OS: {}\n Uptime: {}\n Reload Reason: {}".format(
            ver_dict["host"], ver_dict["model"], ver_dict["os"], ver_dict["up"], ver_dict["reason"]))
    else:
        print('HTTP REQUEST FAILED:\nStatus Code: {}\nReason: {}\nContent: {}'.format(
            sw_ver.status_code, sw_ver.reason, sw_ver.content))


def sh_ver_filter(req):
    """
    This filters the information returned from the show version request
    to just the relevant information (Hostname, Model, OS Version, Uptime,
    and reason for last Reload). Try and except are used for the uptime,
    as the dictionary key will not exist if the switch has not been up
    long enough to increment the specific time value, which will then
    raise an error.

    :param req: The results of an API request for "show versoin"

    :return: A dictionary of "show version" information.
    """
    sw_version = req.json()["result"]["body"]
    try:
        hours = sw_version["kern_uptm_hrs"]
    except:
        hours = 0
    try:
        days = sw_version["kern_uptm_days"]
    except:
        days = 0
    try:
        months = sw_version["kern_uptm_months"]
    except:
        months = 0
    try:
        years = sw_version["kern_uptm_years"]
    except:
        years = 0
    return {
        "host": sw_version["host_name"],
        "model": sw_version["chassis_id"],
        "up": "{} years, {} months, {} days, {} hours, {} minutes, {} seconds".format(
            years, months, days, hours, sw_version["kern_uptm_mins"],
            sw_version["kern_uptm_secs"]),
        "os": sw_version["kickstart_ver_str"],
        "reason": sw_version["rr_reason"]
    }


if __name__ == '__main__':
    main(argv[1])
