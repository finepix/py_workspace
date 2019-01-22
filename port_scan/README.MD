# 寻找当前局域网内的linux主机
step 1：获取当前的ip地址以及子网掩码，得到当前的ip段；
step 2：从最小的ip地址开始ping，得到能ping通的地址；
step 3：使用telnet ip 22 测试其22端口信息；
step 4：汇总，得到需要的地址。
# 需要安装的包
 - IPy（用于处理IP地址的模块）
 - netifaces（用于获取子网掩码以及IP地址，具体详情移步：https://pypi.org/project/netifaces/）
 - 需要用到subprocess