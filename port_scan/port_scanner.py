import os
import telnetlib
from IPy import IP
import netifaces as ntf


def get_localhost_info():
    """
                获取本机的IP地址以及子网掩码，从而得到该局域网的网段
    :return:  本机IP地址（局域网），子网掩码，所在网段
    """
    interfaces = ntf.interfaces()
    eth0_interface = interfaces[0]
    eth0_info = ntf.ifaddresses(eth0_interface)
    # 这里的info为一个字典，-1000为mac地址，23为ipv6信息，2为ipv4信息
    # print(eth0_info)
    ipv4_info = eth0_info[2][0]
    # print(ipv4_info)

    # 获取IP地址以及子网掩码，并得到局域网的网段
    ipv4_address = ipv4_info['addr']
    ipv4_net_mask = ipv4_info['netmask']
    network_segment = IP(ipv4_address).make_net(ipv4_net_mask).strNormal(0)
    # print(network_segment)

    return [ipv4_address, ipv4_net_mask, network_segment]


def ping(ip):
    """
            检测给定ip地址是否能ping通
    :param ip:
    :return:
    """
    cmd = 'ping -w 2 -n 1 {}'.format(ip)
    ping_result_code = os.system(cmd)
    print(ping_result_code)
    if ping_result_code:
        return False
    else:
        return True


def telnet(ip, port=22):
    """
                对于给定ip地址以及端口，使用telnet命令
    :param ip:
    :param port:
    :return:
    """
    try:
        tn = telnetlib.Telnet(ip, port, timeout=10)
        print(tn)
    except Exception as _:
        print('telnet异常捕获。')
        return False
    return True


if __name__ == '__main__':

    [ip_address, net_mask, net_segment] = get_localhost_info()

    # 遍历整个网段

    # ping(ip_address)
    # telnet(ip_address)

