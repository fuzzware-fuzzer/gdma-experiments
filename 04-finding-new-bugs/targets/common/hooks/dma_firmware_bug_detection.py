from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R4, UC_ARM_REG_R9)

"""
To use these hooks add the config snippet associated with each CVE, then
cd to the the .../04-finding-new-bugs/targets directory and
set the following nevironment variable:
export PYTHONPATH=common
"""

"""
Contiki-ng CVE-2022-48229 hooks
Config entry:
handlers:
  bug_checker_1:
    addr: 0x4900
    handler: hooks.dma_firmware_bug_detection.cve_2023_48229_1
    do_return: False

  bug_checker_2:
    addr: 0x4938
    handler: hooks.dma_firmware_bug_detection.cve_2023_48229_2
    do_return: False
"""

CONTIKI_BUFSIZE = -1
def cve_2023_48229_1(uc):
    global CONTIKI_BUFSIZE
    CONTIKI_BUFSIZE = uc.reg_read(UC_ARM_REG_R1)
    return


def cve_2023_48229_2(uc):
    if CONTIKI_BUFSIZE == -1:
        return
    payload_len = uc.reg_read(UC_ARM_REG_R1) - 2
    if payload_len > CONTIKI_BUFSIZE:
        print('[dma_firmware_bug_detection] Heureka! Found CVE-2023-48229')


"""
MBED OS CVE 2024-48981
https://github.com/ARMmbed/mbed-os/issues/15462
Config entry:
handlers:
  bug_checker_1:
    addr: 0x1c7c2
    do_return: false
    handler: hooks.dma_firmware_bug_detection.cve_2024_48981_1
"""
def cve_2024_48981_1(uc):
    iRx = int.from_bytes(uc.mem_read(0x20004c0c, 2), "little")  # address of iRx static variable
    # index is larger than buffer size of 4
    if iRx > 3:
        print('[dma_firmware_bug_detection] Heureka! Found CVE-2024-48981')


"""
MBED OS CVE 2024-48982
https://github.com/mbed-ce/mbed-os/pull/386
Config entry:
handlers:
  bug_checker_1:
    addr: 0x13f38
    do_return: false
    handler: hooks.dma_firmware_bug_detection.cve_2024_48982_1
"""
def cve_2024_48982_1(uc):
    len = uc.reg_read(UC_ARM_REG_R9)
    if len < 3 or len > 0xfd:
        # either integer underflow or overflow
        print('[dma_firmware_bug_detection] Heureka! Found CVE-2024-48982')


"""
https://github.com/mbed-ce/mbed-os/pull/388
MBED OS CVE 2024-48983
Config entry:
handlers:
  bug_checker_1:
    addr: 0x1c06c
    do_return: false
    handler: hooks.dma_firmware_bug_detection.cve_2024_48983_1
  bug_checker_2:
    addr: 0x1c05c
    do_return: false
    handler: hooks.dma_firmware_bug_detection.cve_2024_48983_2
  bug_checker_3:
    addr: 0x1c7e2
    do_return: false
    handler: hooks.dma_firmware_bug_detection.cve_2024_48983_3
  bug_checker_4:
    addr: 0x1c7f6
    do_return: false
    handler: hooks.dma_firmware_bug_detection.cve_2024_48983_4
"""
UINT16_MAX = 2**16 - 1
def cve_2024_48983_1(uc):
    len_var = uc.reg_read(UC_ARM_REG_R0) & 0xffff
    tailroom = uc.reg_read(UC_ARM_REG_R1) & 0xff
    if len_var > UINT16_MAX - tailroom:
        print('[dma_firmware_bug_detection] Heureka! Found CVE-2024-48983 (1)')

def cve_2024_48983_2(uc):
    len_var = uc.reg_read(UC_ARM_REG_R0) & 0xffff
    sizeof_wsfmsg = 8
    if len_var > UINT16_MAX - sizeof_wsfmsg:
        print('[dma_firmware_bug_detection] Heureka! Found CVE-2024-48983 (2)')

def cve_2024_48983_3(uc):
    hdrlen = uc.reg_read(UC_ARM_REG_R0) & 0xff
    data_ptr = uc.reg_read(UC_ARM_REG_R2)
    datalen = int.from_bytes(uc.mem_read(data_ptr + 2, 1), "big")
    if hdrlen > UINT16_MAX - datalen:
        print('[dma_firmware_bug_detection] Heureka! Found CVE-2024-48983 (3)')

def cve_2024_48983_4(uc):
    # replicate the calculation done in assembly and check for overflow at the end
    data_ptr = uc.reg_read(UC_ARM_REG_R2)
    hdrlen = int.from_bytes(uc.mem_read(data_ptr + 3, 1), "big")
    datalen = int.from_bytes(uc.mem_read(data_ptr + 2, 1), "big")
    r1 = uc.reg_read(UC_ARM_REG_R1) & 0xffff
    sum_of_lens = ((hdrlen + (datalen << 8)) & 0xffff) + r1

    if sum_of_lens > UINT16_MAX:
        print('[dma_firmware_bug_detection] Heureka! Found CVE-2024-48983 (4)')


"""
MBED OS CVE 2024-48985
https://github.com/mbed-ce/mbed-os/pull/384
Config entry:
handlers:
  bug_checker_1:
    addr: 0x1c818
    do_return: false
    handler: hooks.dma_firmware_bug_detection.cve_2024_48985_1
"""
def cve_2024_48985_1(uc):
    pPktRx = uc.reg_read(UC_ARM_REG_R0)
    if pPktRx == 0:
        print('[dma_firmware_bug_detection] Heureka! Found CVE-2024-48985')


"""
MBED OS CVE 2024-48986
https://github.com/mbed-ce/mbed-os/pull/385
Config entry:
handlers:
  bug_checker_1:
    addr: 0x139e2
    do_return: false
    handler: hooks.dma_firmware_bug_detection.cve_2024_48986_1
"""
def cve_2024_48986_1(uc):
    len = uc.reg_read(UC_ARM_REG_R2)
    if len > 1:
        print('[dma_firmware_bug_detection] Heureka! Found CVE-2024-48986')
