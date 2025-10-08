# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_nco_project(dut):
    dut._log.info("Starting NCO Testbench")

    # Start 50MHz clock → 20ns period
    clock = Clock(dut.clk, 20, units="ns")
    cocotb.start_soon(clock.start())

    # Initialize signals
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    # Apply reset for few cycles
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    dut._log.info("Reset released")

    # Test 1: Set control word = 3'b001
    dut.ui_in.value = 0b00000001
    await ClockCycles(dut.clk, 100)
    val1 = int(dut.uo_out.value)
    dut._log.info(f"Wave output for control=1: {val1}")

    # Test 2: Set control word = 3'b010
    dut.ui_in.value = 0b00000010
    await ClockCycles(dut.clk, 100)
    val2 = int(dut.uo_out.value)
    dut._log.info(f"Wave output for control=2: {val2}")

    # Optional: Ensure outputs differ (frequency should change)
    assert val1 != val2, "Waveform output did not change with frequency control!"

    # Test 3: Sweep through all control values
    for i in range(8):
        dut.ui_in.value = i
        await ClockCycles(dut.clk, 50)
        dut._log.info(f"ui_in={i:03b}, uo_out={int(dut.uo_out.value)}")

    dut._log.info("NCO test completed successfully")
