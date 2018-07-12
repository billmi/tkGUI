#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wmi
import sys, time, platform


def get_system_info(os):
    """
    获取操作系统版本。
    """
    print("Operating system:")
    if os == "Windows":
        c = wmi.WMI()
        for sys in c.Win32_OperatingSystem():
            print('\t' + "Version :\t%s" % sys.Caption.encode("GBK"))
            print('\t' + "Vernum :\t%s" % sys.BuildNumber)


def get_memory_info(os):
    """
    获取物理内存和虚拟内存。
    """
    print("memory_info:")
    if os == "Windows":
        c = wmi.WMI()
        cs = c.Win32_ComputerSystem()
        pfu = c.Win32_PageFileUsage()
        MemTotal = int(cs[0].TotalPhysicalMemory) / 1024 / 1024
        print('\t' + "TotalPhysicalMemory :" + '\t' + str(MemTotal) + "M")
        # tmpdict["MemFree"] = int(os[0].FreePhysicalMemory)/1024
        SwapTotal = int(pfu[0].AllocatedBaseSize)
        print('\t' + "SwapTotal :" + '\t' + str(SwapTotal) + "M")
        # tmpdict["SwapFree"] = int(pfu[0].AllocatedBaseSize - pfu[0].CurrentUsage)


def get_disk_info(os):
    """
    获取物理磁盘信息。
    """
    print("disk_info:")
    if os == "Windows":
        tmplist = []
        c = wmi.WMI()
        for physical_disk in c.Win32_DiskDrive():
            if physical_disk.Size:
                print('\t' + str(physical_disk.Caption) + ' :\t' + str(
                    int(physical_disk.Size) / 1024 / 1024 / 1024) + "G" + "\t" + physical_disk.SerialNumber.strip()
                      )


def get_board_info(os):
    """
     获取主板序列号。
     """
    print("board_info:")
    if os == "Windows":
        tmplist = []
        c = wmi.WMI()
        for board_id in c.Win32_BaseBoard():
            # encrypt_str = encrypt_str + board_id.SerialNumber.strip()
            print("main board id:", board_id.SerialNumber.strip())


def get_cpu_info(os):
    """
    获取CPU信息。
    """
    print("cpu_info:")
    if os == "Windows":
        tmpdict = {}
        tmpdict["CpuCores"] = 0
        c = wmi.WMI()
        for cpu in c.Win32_Processor():
            tmpdict["CpuType"] = cpu.Name
        try:
            tmpdict["CpuCores"] = cpu.NumberOfCores
        except:
            tmpdict["CpuCores"] += 1
            tmpdict["CpuClock"] = cpu.MaxClockSpeed
        print('\t' + 'CpuType :\t' + str(tmpdict["CpuType"]))
        print('\t' + 'CpuCores :\t' + str(tmpdict["CpuCores"]))


def get_network_info(os):
    """
    获取网卡信息和当前TCP连接数。
    """
    print("network_info:")
    if os == "Windows":
        tmplist = []
        c = wmi.WMI()
        for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=1):
            tmpdict = {}
            tmpdict["Description"] = interface.Description
            tmpdict["IPAddress"] = interface.IPAddress[0]
            tmpdict["IPSubnet"] = interface.IPSubnet[0]
            tmpdict["MAC"] = interface.MACAddress
            tmplist.append(tmpdict)
        for i in tmplist:
            print('\t' + i["Description"])
            print('\t' + '\t' + "MAC :" + '\t' + i["MAC"])
            print('\t' + '\t' + "IPAddress :" + '\t' + i["IPAddress"])
            print('\t' + '\t' + "IPSubnet :" + '\t' + i["IPSubnet"])
        for interfacePerfTCP in c.Win32_PerfRawData_Tcpip_TCPv4():
            print('\t' + 'TCP Connect :\t' + str(interfacePerfTCP.ConnectionsEstablished))


if __name__ == "__main__":
    os = platform.system()
    get_board_info(os)
    get_system_info(os)
    get_memory_info(os)
    get_disk_info(os)
    get_cpu_info(os)
    get_network_info(os)
