#==========================================================================================
# TestCase
#==========================================================================================
from cocotb.handle import *
from SimEnv import *
import random
@cocotb.test()
async def test0(dut):
    simEnv=SimEnv(dut=dut)
    await simEnv.start()
    for index in range(50):
        obj=DataTransactoin()
        obj.data0=random.randint(0, 1<<16)
        obj.data1=random.randint(0, 1<<16)
        await simEnv.send(obj)
    cocotb.log.info("wait done")
    await simEnv.wait(coverage_xml="test0_coverage")

@cocotb.test()
async def test1(dut):
    simEnv=SimEnv(dut=dut)
    await simEnv.start()
    for index in range(50):
        obj=DataTransactoin()
        obj.data0=0
        obj.data1=0xffff
        await simEnv.send(obj)
    cocotb.log.info("wait done")
    await simEnv.wait(coverage_xml="test1_coverage")
    merge_coverage(cocotb.log.info,"all.xml","test1_coverage.xml","test0_coverage.xml")