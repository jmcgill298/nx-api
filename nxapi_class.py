import requests
from getpass import getpass


def req_body(cmd):
    return {
        "jsonrpc": "2.0",
        "method": "cli",
        "id": 1,
        "params": {
            "cmd": cmd,
            "version": 1
        }
    }


class NxAaa:
    """
    This class is used to gather a authentication Cookie.
    This cookie can then be passed for each request used
    to interact with the switch, instead of logging in
    each time.
    """

    def __init__(self, user, switch, passw=None):
        """
        This initializes a switch login object.
        :param user: The username used to login.
        :param passw: The password for the users;
        defaults to using getpass for security.
        :param switch: The switch to connect to.
        """
        self.user = user

        if passw is None:
            self.passw = getpass('What is your password: ')
        else:
            self.passw = passw

        self.switch = switch

    def nx_login(self):
        """
        This method is used to login to the switch and
        return a header with cookie for future interactions.

        :return: A header with content type and cookie.

        :example:
        >>> switch = NxAaa('user', '10.1.1.1')
        What is your password:
        >>> switch_login = switch.nx_login()
        >>> print(switch_login)
        {'Cookie': 'nxapi_auth=user:148095010189978541', 'content-type': 'application/json-rpc'}
        """
        requests.packages.urllib3.disable_warnings()
        url = "https://{}/ins".format(self.switch)
        header = {"content-type": "application/json-rpc"}
        body = req_body("show version")

        header["Cookie"] = requests.post(url, json=body, headers=header,
                                         auth=(self.user, self.passw), verify=False).headers["Set-Cookie"]

        return header


class NxSystem:
    def __init__(self, header, switch, url=None):
        """
        This initializes a NX-OS object for interacting
        with the system parameters.

        :param header: The header from NxAAA.nx_login().
        :param switch: The switch to interact with.
        :param url: The url to post to; leaving to None
        should configure the appropriate URL.
        """
        self.header = header
        self.switch = switch
        if url is None:
            self.url = 'https://{}/ins'.format(switch)
        else:
            self.url = url

    def nx_sh_ver(self):
        """
        This method is used to collect the "show version" data.

        :return: This returns the results from a http request
        to collect switch version information.

        :example:
        >>> switch_system = NxSystem(switch_login, '10.1.1.1')
        >>> switch_version = switch_system.nx_sh_ver()
        >>> pprint(switch_version.json())
        {'id': 1,
        'jsonrpc': '2.0',
        'result': {
            'body': {
                'bios_cmpl_time': '08/26/2016',
                'bios_ver_str': '07.59',
                'bootflash_size': 21693714,
                'chassis_id': 'Nexus9000 C9396PX Chassis',
                'cpu_name': 'Intel(R) Core(TM) i3- CPU @ 2.50GHz',
                'header_str': ...
                'host_name': 'switch1',
                'kern_uptm_days': 16,
                'kern_uptm_hrs': 10,
                'kern_uptm_mins': 11,
                'kern_uptm_secs': 27,
                'kick_cmpl_time': ' 10/29/2016 6:00:00',
                'kick_file_name': 'bootflash:///nxos.7.0.3.I5.1.bin',
                'kick_tmstmp': '10/29/2016 13:46:41',
                'kickstart_ver_str': '7.0(3)I5(1)',
                'manufacturer': 'Cisco Systems, Inc.',
                'mem_type': 'kB',
                'memory': 16401440,
                'proc_board_id': 'SAL1824UGVA',
                'rr_ctime': ' Sat Nov 19 04:42:17 2016\n',
                'rr_reason': 'Power Down/UP epld upgrade process',
                'rr_service': 'Power Down/UP epld upgrade process',
                'rr_usecs': 41368
            }
        }}
        """
        body = req_body('show version')

        return requests.post(self.url, json=body, headers=self.header, verify=False)


class NxL2:
    def __init__(self, header, switch, vlan=None, url=None):
        """
        This initializes a NX-OS object for interacting with
        Layer 2 parameters.

        :param header: The header from NxAAA.nx_login().
        :param switch: The switch to interact with.
        :param vlan: The VLAN ID if configuring or interacting
        with a particular VLAN.
        :param url: The url to post to; leaving to None
        should configure the appropriate URL.
        """
        self.header = header
        self.switch = switch
        self.vlan = vlan
        if url is None:
            self.url = 'https://{}/ins'.format(switch)
        else:
            self.url = url

    def sh_vlan(self):
        """
        This method is used to collect the "show vlan" data.

        :return: This returns the results from a http request
        to collect switch VLAN information.

        :example:
        >>> switch_vlan = NxL2(switch_login, '10.1.1.1', '10')
        >>> sh_vlans = switch_vlan.sh_vlan()
        >>> pprint(sh_vlans.json())
        {'id': 1,
        'jsonrpc': '2.0',
        'result': {
            'body': {
                'TABLE_mtuinfo': {
                    'ROW_mtuinfo': [
                        {
                            'vlanshowinfo-media-type': 'enet',
                            'vlanshowinfo-vlanid': '1',
                            'vlanshowinfo-vlanmode': 'ce-vlan'
                        },
                        {
                            'vlanshowinfo-media-type': 'enet',
                            'vlanshowinfo-vlanid': '10',
                            'vlanshowinfo-vlanmode': 'ce-vlan'
                        },
                        {
                            'vlanshowinfo-media-type': 'enet',
                            'vlanshowinfo-vlanid': '20',
                            'vlanshowinfo-vlanmode': 'ce-vlan'
                        }
                    ]
                },
                'TABLE_vlanbrief': {
                    'ROW_vlanbrief': [
                    {
                        'vlanshowbr-shutstate': 'noshutdown',
                        'vlanshowbr-vlanid': '1',
                        'vlanshowbr-vlanid-utf': '1',
                        'vlanshowbr-vlanname': 'default',
                        'vlanshowbr-vlanstate': 'active',
                        'vlanshowplist-ifidx': 'Ethernet1/1,Ethernet1/2,Ethernet1/3,Ethernet1/4,
                        Ethernet1/5,Ethernet1/6,Ethernet1/7,Ethernet1/8,Ethernet1/9,Ethernet1/10,
                        Ethernet1/11,Ethernet1/12,Ethernet1/13,Ethernet1/14,Ethernet1/15,Ethernet1/16,
                        Ethernet1/17,Ethernet1/18,Ethernet1/19,Ethernet1/20,Ethernet1/21,Ethernet1/22,
                        Ethernet1/23,Ethernet1/24,Ethernet1/25,Ethernet1/26,Ethernet1/27,Ethernet1/28,
                        Ethernet1/29,Ethernet1/30,Ethernet1/31,Ethernet1/32,Ethernet1/33,Ethernet1/34,
                        Ethernet1/35,Ethernet1/36,Ethernet1/37,Ethernet1/38,Ethernet1/39,Ethernet1/40,
                        Ethernet1/41,Ethernet1/42,Ethernet1/43,Ethernet1/44,Ethernet1/46,Ethernet1/48,
                        Ethernet2/1,Ethernet2/2,Ethernet2/3,Ethernet2/4,Ethernet2/5,Ethernet2/6,
                        Ethernet2/7,Ethernet2/8,Ethernet2/9,Ethernet2/10,Ethernet2/11,Ethernet2/12'
                    },
                    {
                        'vlanshowbr-shutstate': 'noshutdown',
                        'vlanshowbr-vlanid': '10',
                        'vlanshowbr-vlanid-utf': '10',
                        'vlanshowbr-vlanname': 'web',
                        'vlanshowbr-vlanstate': 'active',
                        'vlanshowplist-ifidx': 'Ethernet1/45,Ethernet1/47'
                    },
                    {
                        'vlanshowbr-shutstate': 'noshutdown',
                        'vlanshowbr-vlanid': '20',
                        'vlanshowbr-vlanid-utf': '20',
                        'vlanshowbr-vlanname': 'database',
                        'vlanshowbr-vlanstate': 'active'
                    }
                ]
            }
        }}}
        """
        body = req_body('show vlan')

        return requests.post(self.url, json=body, headers=self.header, verify=False)

    def sh_vlan_id(self, vlan=None):
        """
        This method is used to collect the "show vlan" data
        for a particular VLAN.

        :param vlan: The VLAN ID to view; defaults to VLAN
        used to initialize the object.

        :return: This returns the results from a http request
        to collect the specific VLAN information.

        :example:
        >>> sh_vlan = switch_vlan.sh_vlan_id()
        >>> pprint(sh_vlan.json())
        {'id': 1,
         'jsonrpc': '2.0',
          'result': {
              'body': {
                  'TABLE_mtuinfoid': {
                      'ROW_mtuinfoid': {
                          'vlanshowinfo-media-type': 'enet',
                          'vlanshowinfo-vlanid': '10',
                          'vlanshowinfo-vlanmode': 'ce-vlan'
                      }
                  },
                  'TABLE_vlanbriefid': {
                      'ROW_vlanbriefid': {
                          'vlanshowbr-shutstate': 'noshutdown',
                          'vlanshowbr-vlanid': '10',
                          'vlanshowbr-vlanid-utf': '10',
                          'vlanshowbr-vlanname': 'web',
                          'vlanshowbr-vlanstate': 'active',
                          'vlanshowplist-ifidx': 'Ethernet1/45,Ethernet1/47'
                      }
                  },
                  'is-vtp-manageable': 'enabled',
                  'vlanshowrspan-vlantype': 'notrspan'
              }
          }}
        """
        if vlan is None:
            vlan = self.vlan

        body = req_body("show vlan id {}".format(vlan))

        return requests.post(self.url, json=body, headers=self.header, verify=False)

    def conf_vlan(self, name, vlan=None):
        """
        This method is used to create a new VLAN ID on a switch.

        :param name: The name of the new VLAN
        :param vlan: The VLAN ID to view; defaults to VLAN
        used to initialize the object.

        :return: This returns the results from a http request
        to configure the new VLAN.

        :example:
        >>> switch_l2 = NxL2(switch_login, '10.1.1.1', '20')
        >>> switch_vlan_conf = switch_l2.conf_vlan('database')
        >>> print("\nRequest returned {} {}\n{} created.".format(
        switch_vlan_conf.status_code, switch_vlan_conf.reason,
        json.loads(vlan_conf.request.body.decode())[1]['params']['cmd'].upper()))

        Request returned 200 OK
        VLAN 20 created.
        """
        if vlan is None:
            vlan = self.vlan

        body = [req_body('conf t'), req_body('vlan {}'.format(vlan)),
                req_body('name {}'.format(name))]

        return requests.post(self.url, json=body, headers=self.header, verify=False)


class NxIntfc:
    def __init__(self, header, switch, intfc=None, url=None):
        """
        This initializes a NX-OS object for interacting with interfaces.

        :param header: The header from NxAAA.nx_login().
        :param switch: The switch to interact with.
        :param intfc: The particular interface to interact with.
        :param url: The url to post to; leaving to None should
        configure the appropriate URL.
        """
        self.header = header
        self.switch = switch
        self.intfc = intfc
        if url is None:
            self.url = 'https://{}/ins'.format(switch)
        else:
            self.url = url

    def sh_intfcs(self):
        """
        This method is used to collect "show interface" results.

        :return: This returns the results from an http request
        to display "show interfaces."

        :example:
        >>> sw_intfcs = NxIntfc(switch_login, '10.1.1.1', 'eth1/48')
        >>> sw_sh_intfcs = sw_intfcs.sh_intfcs()
        >>> pprint(sw_sh_intfcs.json()['result']['body']['TABLE_interface']['ROW_interface'])
        {
            "interface": "mgmt0",
            "state": "up",
            "admin_state": "up",
            "eth_hw_desc": "GigabitEthernet",
            "eth_hw_addr": "5087.89d4.32de",
            "eth_bia_addr": "5087.89d4.32de",
            "eth_ip_addr": "10.1.1.1",
            "eth_ip_mask": 25,
            "eth_ip_prefix": "100",
            "eth_mtu": "1500",
            "eth_bw": 1000000,
            "eth_dly": 10,
            "eth_reliability": "255",
            "eth_txload": "1",
            "eth_rxload": "1",
            "medium": "broadcast",
            "eth_duplex": "full",
            "eth_speed": "1000 Mb/s",
            "eth_autoneg": "off",
            "eth_mdix": "off",
            "eth_ethertype": "0x0000",
            "vdc_lvl_in_avg_bits": 1192,
            "vdc_lvl_in_avg_pkts": "1",
            "vdc_lvl_out_avg_bits": "6096",
            "vdc_lvl_out_avg_pkts": "1",
            "vdc_lvl_in_pkts": 1532699,
            "vdc_lvl_in_ucast": "25288",
            "vdc_lvl_in_mcast": "1442435",
            "vdc_lvl_in_bcast": "64976",
            "vdc_lvl_in_bytes": "157494301",
            "vdc_lvl_out_pkts": "59631",
            "vdc_lvl_out_ucast": "27913",
            "vdc_lvl_out_mcast": "31715",
            "vdc_lvl_out_bcast": "3",
            "vdc_lvl_out_bytes": "14022666"
          },
          {
          ...
          }
        }
        """
        body = req_body('show interface')

        return requests.post(self.url, json=body, headers=self.header, verify=False)
