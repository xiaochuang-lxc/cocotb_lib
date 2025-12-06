#!/usr/bin/python3
import os
import sys
current_file_path = os.path.abspath(__file__)
# 获取当前文件所在目录的绝对路径
current_dir_path = os.path.dirname(current_file_path)
# 获取当前文件的父目录的父目录的绝对路径
parent_parent_dir_path = os.path.dirname(current_dir_path)
# 将父目录的父目录的绝对路径添加到 sys.path
sys.path.append(parent_parent_dir_path)
from stream.stream_ext import *
from cocotb.handle import *
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
from cocotb.queue import Queue
from cocotb_coverage.coverage import *
#==========================================================================================
# Source,Sink定义 
#==========================================================================================
item_map={"data0":(0,16),"data1":(16,16)}
DataBus,DataTransactoin,DataSource,DataSink,DataMonitor=define_streamext(name="Data",item_map=item_map)
#==========================================================================================
# SimEnv
#==========================================================================================
class SimEnv(object):
    def __init__(self,dut:SimHandleBase):
        self.dut=dut
        self.clk=dut.clk
        self.port_in_mst=DataSource(bus=DataBus(entity=self.dut, prefix="data_in"),clock=self.dut.clk)
        self.port_out_slv=DataSink(bus=DataBus(entity=self.dut, prefix="data_out"),clock=self.dut.clk)
        self.clk_th=cocotb.start_soon(Clock(signal=dut.clk,period=4,units='ns').start())
        self.refQueue=Queue()
    
    async def start(self):
        await self._reset()
        self.dut_cover_sample_th=cocotb.start_soon(self.dut_cover_sample())
        self.port_out_slv.add_callback(self.data_check)
        self.port_out_slv.open_only_exec_callback()

    async def _reset(self):
        self.dut.reset.value = 1
        await ClockCycles(signal=self.clk,num_cycles=10)
        self.dut.reset.value = 0

    async def wait(self,coverage_xml):
        await self.port_in_mst.wait()
        await self.port_out_slv.wait()
        while not self.refQueue.empty():
            cocotb.log.info(f"current {self.refQueue.qsize()}")
            await ClockCycles(signal=self.clk,num_cycles=10)
        coverage_db.export_to_xml(filename=f"{coverage_xml}.xml")
    # 输入激励采样
    data_in_cover_section=coverage_section(
        CoverPoint(name="top.data_in_0",xf=lambda trans:trans.data0,bins=[(0,0),(1,0xfffe),(0xffff,0xffff)],rel=lambda value,bin:bin[0]<=value<=bin[1],bins_labels=["all_zero","random","all_one"]),
        CoverPoint(name="top.data_in_1",xf=lambda trans:trans.data1,bins=[(0,0),(1,0xfffe),(0xffff,0xffff)],rel=lambda value,bin:bin[0]<=value<=bin[1],bins_labels=["all_zero","random","all_one"])
    )
    @data_in_cover_section
    async def send(self,trans):
        ref_obj=DataTransactoin()
        ref_obj.data0=(trans.data0+trans.data1)&0xffff
        ref_obj.data1=0
        self.refQueue.put_nowait(ref_obj)
        await self.port_in_mst.send(trans)
        self.port_in_mst.log.info(f"send a cmd :{trans}")
    

    @CoverPoint(name="top.data_out_0",xf=lambda recv_obj:recv_obj.data0,bins=[(0,0),(1,0xfffe),(0xffff,0xffff)],rel=lambda value,bin:bin[0]<=value<=bin[1],bins_labels=["all_zero","random","all_one"])
    def data_check(self,recv_obj):
        ref_result=self.refQueue.get_nowait()
        assert recv_obj==ref_result
    
    # dut内部信号采样覆盖
    dut_cover_section=coverage_section(
        CoverPoint(name="dut.data_in_translated_valid",xf=lambda dut:dut.data_in_translated_valid,bins=[0,1],bins_labels=["LOW","HIGH"]),
        CoverPoint(name="dut.data_in_translated_ready",xf=lambda dut:dut.data_in_translated_ready,bins=[0,1],bins_labels=["LOW","HIGH"]),
        CoverCross(name="dut.data_in_translated_state",items=["dut.data_in_translated_valid","dut.data_in_translated_ready"])
    )
    @dut_cover_section
    def dut_cover(self,dut):
        pass
    
    async def dut_cover_sample(self):
        while True:
            await RisingEdge(self.dut.clk)
            self.dut_cover(self.dut)