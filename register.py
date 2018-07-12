import base64
import sys
from pyDes import *
import wmi
import datetime
import hashlib
import uuid


class ZyylRegister:
    FUNC_TYPES_DICT = {
        'counts': 1,
        'months': 2
    }

    def __init__(self):
        self.Des_Key = b"#UC#@*)M"  # Key
        self.Des_IV = b"\x22\x33\x35\x81\xBC\x38\x5A\xE7"  # IV向量
        self.RegisterCode = ''

    # 获取硬盘序列
    def GetDiskInfo(self):
        physicalSerialNumber = ''
        # print("disk_info:")
        c = wmi.WMI()
        for physical_disk in c.Win32_DiskDrive():
            physicalSerialNumber = physical_disk.SerialNumber.strip()
            break
            # print("Physical Serial Number:", physicalSerialNumber)
        return physicalSerialNumber

    # 获取主板序列
    def GetBoardInfo(self):
        # print("board_info:")
        boardID = ''
        c = wmi.WMI()
        for board_id in c.Win32_BaseBoard():
            # encrypt_str = encrypt_str + board_id.SerialNumber.strip()
            boardID = board_id.SerialNumber.strip()
            # print("main board id:", boardID)
        return boardID

    # 获取Mac地址
    def GetMacAddress(self):
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return "".join([mac[e:e + 2] for e in range(0, 11, 2)])

    # 获取CPU列号
    def GetCpuNumber(self):
        c = wmi.WMI()
        cpuid = ""
        for cpu in c.Win32_Processor():
            cpuid = cpuid + cpu.ProcessorId.strip()
        return cpuid

    def DesEncrypt(self, str):
        k = des(self.Des_Key, CBC, self.Des_IV, pad=None, padmode=PAD_PKCS5)
        EncryptStr = k.encrypt(str)
        # EncryptStr = binascii.unhexlify(k.encrypt(str))
        return base64.b64encode(EncryptStr)

    # des解码
    def DesDecrypt(self, str):
        src = base64.b64decode(str)
        k = des(self.Des_Key, CBC, self.Des_IV, pad=None, padmode=PAD_PKCS5)
        DecryptStr = k.decrypt(src)
        # print (DecryptStr)
        return DecryptStr

    def GetRegistCode(self, userdecode):
        if userdecode:
            uCode = self.GetUserCode()
            encodeInfo = uCode + '|||' + userdecode
            self.key_encrypted = self.DesEncrypt(encodeInfo).decode()
            self.SaveRegisterCode()
            return self.key_encrypted
        else:
            return ""

    def GetUserCodeFromKey(self, needDesCode):
        sourcecode = self.DesDecrypt(needDesCode).decode()
        return sourcecode.split('|||')[0]

    def GetRegCodeFromKey(self, needDesCode):
        sourcecode = self.DesDecrypt(needDesCode).decode()
        return sourcecode.split('|||')[1]

    def ValiUserCodeFromKey(self, needDesCode):
        result = False
        try:
            sourcecode = self.DesDecrypt(needDesCode).decode()
            uCode = sourcecode.split('|||')[0]
            currCode = self.GetUserCode()
            if currCode == uCode:
                result = True
        except Exception as e:
            pass
        finally:
            return result

    def GetUserCode(self):
        cpuNumber = self.GetCpuNumber()
        diskNumber = self.GetDiskInfo()
        boardNumber = self.GetBoardInfo()
        sourcestr = cpuNumber + '|' + diskNumber + '|' + boardNumber
        md5 = hashlib.md5()
        md5.update(sourcestr.encode('utf-8'))
        codeSrc = md5.hexdigest()
        usercode = codeSrc[0:4] + '-' + codeSrc[4:10] + '-' + codeSrc[10:16] + '-' + codeSrc[16:22] + '-' + codeSrc[
                                                                                                            22:28] + '-' + codeSrc[
                                                                                                                           28:32]
        return usercode

    def SaveRegisterCode(self):
        with open('./user.license', 'w') as f:
            f.write(self.key_encrypted)
            f.close()

    def GetUserOri(self, needDesCode):
        sourcecode = self.DesDecrypt(needDesCode).decode()
        registerKey = sourcecode.split('|||')[1]
        return registerKey

    def AnalysisUserInfo(self, userInfo):
        uData = {'user': None, 'func': None, 'data': None, 'uid': None}
        infos = userInfo.split("||")
        uData['user'] = infos[0]
        registerInfos = infos[1].split('|')
        uData['uid'] = registerInfos[1]
        funcInfos = registerInfos[0].split('@')
        uData['func'] = funcInfos[0]
        uData['data'] = funcInfos[1]
        return uData

    def IsLegal(self, needDesCode):
        result = False
        try:
            self.DesDecrypt(needDesCode).decode()
            result = True
        except Exception as e:
            pass
        finally:
            return result

    def GetFuncTypeNum(self, funcStr):
        return self.FUNC_TYPES_DICT[funcStr]
