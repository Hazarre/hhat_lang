from __future__ import annotations

from hhat_lang.core.code.ir import InstrIRFlag, TypeIR
from hhat_lang.core.code.utils import InstrStatus
from hhat_lang.core.data.core import CoreLiteral, Symbol
from hhat_lang.core.memory.core import MemoryManager, Stack
from hhat_lang.dialects.heather.code.simple_ir_builder.ir import (
    FnIR,
    IRArgs,
    IRBlock,
    IRInstr,
)
from hhat_lang.dialects.heather.interpreter.classical.executor import Evaluator
from hhat_lang.low_level.quantum_lang.openqasm.v2.instructions import QNot
from hhat_lang.low_level.quantum_lang.openqasm.v2.qlang import LowLeveQLang


# TODO 1
def test_if():
    """
    @v:@u2 = @2
    @if(
    @not(@2): @not(@3)
    @true: @redim(@2)
    )
    """
    mem = MemoryManager(5)
    mem.idx.add(Symbol("@v"), 2)
    mem.idx.request(Symbol("@v"))

    ex = Evaluator(mem, TypeIR(), FnIR())

    # @not(@v)
    cond = IRInstr(
        name=Symbol("@not"),
        args=IRArgs(Symbol("@v")),
        flag=InstrIRFlag.CALL,
    )

    # @not(@3)
    true_instr = IRInstr(
        name=Symbol("@not"),
        args=IRArgs(CoreLiteral("@3", "@u2")),
        flag=InstrIRFlag.CALL,
    )

    # @redim(@v)
    else_instr = IRInstr(
        name=Symbol("@redim"),
        args=IRArgs(Symbol("@v")),
        flag=InstrIRFlag.CALL,
    )

    #
    if_instr = IRInstr(
        name=Symbol("@if"),
        args=IRArgs(cond, true_instr, else_instr),
        flag=InstrIRFlag.CALL,
    )

    block = IRBlock()
    block.add_instr(if_instr)
    qlang = LowLeveQLang(Symbol("@v"), block, mem.idx, ex, Stack())
    res = qlang.gen_program()
    print(res)


def test_gen_program_single_bool_not() -> None:
    code_snippet = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];

x q[0];
measure q -> c;
"""

    mem = MemoryManager(5)
    mem.idx.add(Symbol("@v"), 3)
    mem.idx.request(Symbol("@v"))
    # qv = Symbol("@v", "@u1")
    cl = CoreLiteral("@0", "@u1")
    # mem.heap.set(qv, CoreLiteral("@0", "@u1"))
    ex = Evaluator(mem, TypeIR(), FnIR())

    block = IRBlock()
    block.add_instr(
        IRInstr(
            name=Symbol("@not"),
            args=IRArgs(cl),
            flag=InstrIRFlag.CALL,
        )
    )

    qlang = LowLeveQLang(Symbol("@v"), block, mem.idx, ex, Stack())
    res = qlang.gen_program()
    print(res)
    # assert res == code_snippet


test_gen_program_single_bool_not()
