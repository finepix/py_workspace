import os
import telnetlib
from IPy import IP
import netifaces as ntf
import subprocess
import logging


def get_localhost_info():
    """
                获取本机的IP地址以及子网掩码，从而得到该局域网的网段
    :return:  本机IP地址（局域网），子网掩码，所在网段
    """
    interfaces = ntf.interfaces()
    eth0_interface = interfaces[0]
    eth0_info = ntf.ifaddresses(eth0_interface)
    # 这里的info为一个字典，-1000为mac地址，23为ipv6信息，2为ipv4信息
    # logging.info(eth0_info)
    ipv4_info = eth0_info[2][0]
    # logging.info(ipv4_info)

    # 获取IP地址以及子网掩码，并得到局域网的网段
    ipv4_address = ipv4_info['addr']
    ipv4_net_mask = ipv4_info['netmask']
    network_segment = IP(ipv4_address).make_net(ipv4_net_mask).strNormal(0)
    # logging.info(network_segment)

    return [ipv4_address, ipv4_net_mask, network_segment]


def ping(ip, achieve_type=3):
    """
                检测给定ip地址是否能ping通
    :param ip:
    :param achieve_type: 实现方式，1 、 2
    :return:
    """
    if achieve_type == 1:
        cmd = 'ping -w 2 -n 1 {}'.format(ip)
        ping_result_code = os.system(cmd)
        logging.info(ping_result_code)
        if ping_result_code:
            return False
        else:
            return True
    if achieve_type == 2:
        p = subprocess.Popen(['ping.exe', ip], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             shell=True)
        output = p.stdout.read()
        logging.info(output)
    else:
        cmd = 'ping -w 2 -n 1 {}'.format(ip)
        status_code, output = subprocess.getstatusoutput(cmd)

        logging.info('ping返回状态代码：{}'.format(not status_code))
        # logging.debug(output)

        if status_code == 0:                    # 正确执行
            return True
        else:
            return False


def telnet(ip, port=22, achieve_type=1):
    """
                对于给定ip地址以及端口，使用telnet命令
    :param ip:
    :param port:
    :param achieve_type:
    :return:
    """
    if achieve_type == 1:
        try:
            telnetlib.Telnet(ip, port, timeout=1)
            logging.info('测试通过')
        except Exception as _:
            logging.error(_)

            return False
        return True
    else:
        pass


if __name__ == '__main__':
    # test on telnet
    # telnet('192.168.149.1')

    [_, net_mask, net_segment] = get_localhost_info()

    result = []
    result_ping = []

    # 遍历整个网段，并将结果保存至result
    IPs = IP(net_segment).make_net(net_mask)
    for IP_obj in IPs:
        ip_address = IP_obj.strNormal(0)
        logging.info('开始测试IP地址：{}'.format(ip_address))
        ping_status = ping(ip_address)
        if ping_status:                             # 能ping通的ip
            result_ping.append(ip_address)
            telnet_status = telnet(ip_address)
            if telnet_status:                       # 端口测试通过
                result.append(ip_address)

    logging.info(result_ping)
    logging.info(result)

    # 通过筛选，得到合适的IP地址




