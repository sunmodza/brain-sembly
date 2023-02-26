from __future__ import annotations
from typing import List, Literal, Tuple, Union, Dict
from command import Command, opti_brain
from memory import MemoryUnit
import inspect
import command
import memory


class BrainF:
    def __init__(self, size: int) -> None:
        self._command = ""
        self.memory = []
        self.ptr = 0
        self.registers: List[MemoryUnit] = [regis() for _, regis in inspect.getmembers(
            memory, inspect.isclass) if issubclass(regis, MemoryUnit) and regis != MemoryUnit]
        self.commands: List[Command] = [cmm() for _, cmm in inspect.getmembers(
            command, inspect.isclass) if issubclass(cmm, Command) and cmm != Command]
        self.create_memory(size)
        self.set_command_master()

    def get_memory_location(self, ref: Union[int, str]) -> int:
        if isinstance(ref, str):
            for register in self.registers:
                if register.name == ref:
                    return register.location
        return self.memory[ref].location

    def apply(self, command):
        self._command += command

    def set_command_master(self):
        for command in self.commands:
            command.master = self

    def execute_command(self, cmm: str):
        for command in self.commands:
            if command.check_n_eval(cmm):
                return

    def get_register_position(self, ref: str) -> int:
        return self.registers.get_register_location(ref)

    def create_memory(self, size: int) -> None:
        for position in range(size):
            mem_unit = MemoryUnit(position)
            self.memory.append(mem_unit)

        for register in self.registers:
            register.location = len(self.memory)
            self.memory.append(register)

    def memdir(self, src, dest) -> Tuple(Literal[">", "<"], int, int):
        src, dest = self.get_memory_location(
            src), self.get_memory_location(dest)
        dist = abs(src-dest)
        if src > dest:
            return "<", dist, dest-src
        return ">", dist, dest-src
