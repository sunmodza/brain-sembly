from typing import TYPE_CHECKING, List, Union, Dict
import re

if TYPE_CHECKING:
    from brainf import BrainF


def anti_sign(sign: str) -> str:
    if sign == ">":
        return "<"
    return ">"


def opti_brain(command: str):
    while "<>" in command:
        command = command.replace("<>", "")
    while "><" in command:
        command = command.replace("><", "")
    return command


def remove_nested_square_brackets(text):
    pattern = r'\[[^\[\]]*\]'
    while re.search(pattern, text):
        text = re.sub(pattern, '', text)
    return text


class Command:
    name: str
    args_count: int
    master: 'BrainF'

    def check_n_eval(self, cmm: str):
        data = cmm.split(" ")
        command_name = data[0]
        args = data[1:]
        phd = []
        for value in args:
            if value.lstrip("-").isdigit():
                phd.append(int(value))
            else:
                phd.append(value)
        args = phd

        if command_name == self.name and len(args) == self.args_count:
            return_command = self.eval(*args)
            if return_command:
                self.master.apply(return_command)
            return True
        return False

    def set_master(self, master: 'BrainF') -> None:
        self.master = master

    def eval(self, *args) -> str:
        raise NotImplementedError


class PT(Command):
    name = "PT"
    args_count = 1

    def eval(self, dest):
        direction, distance, dist_true = self.master.memdir(
            self.master.ptr, dest)
        command = direction*distance
        self.master.ptr += dist_true
        return command


class RST(Command):
    name = "RST"
    args_count = 0

    def eval(self):
        command = "[-]"
        return command


class MOV(Command):
    name = "MOV"
    args_count = 1

    def eval(self, dest):
        sign, dist, _ = self.master.memdir(self.master.ptr, dest)
        command = f"[-{sign*dist}+{anti_sign(sign)*dist}]"
        return command


class CPY(Command):
    name = "CPY"
    args_count = 1

    def eval(self, dest):
        src = self.master.ptr
        self.master.execute_command("MOV CBAR")
        self.master.execute_command("PT CBAR")

        sign_dest, dist_dest, _ = self.master.memdir("CBAR", dest)
        sign_src, dist_src, _ = self.master.memdir("CBAR", src)
        command = f"[-{sign_dest*dist_dest}+{anti_sign(sign_dest)*dist_dest}{sign_src*dist_src}+{anti_sign(sign_src)*dist_src}]"
        # self.master.execute_command("RST")
        self.master.apply(command)
        self.master.execute_command("RST")
        self.master.execute_command(f"PT {src}")
        return ""


class INPUT(Command):
    name = "INPUT"
    args_count = 0

    def eval(self) -> str:
        src = self.master.ptr
        self.master.execute_command("PT IX")
        self.master.apply(",")
        self.master.execute_command(f"PT {src}")
        return ""


class OUTPUT(Command):
    name = "OUTPUT"
    args_count = 0

    def eval(self) -> str:
        base = self.master.ptr
        self.master.execute_command("PT APX")
        self.master.apply(".")
        self.master.execute_command(f"PT {base}")
        return ""


class ADDN(Command):
    name = "ADDN"
    args_count = 1

    def eval(self, num: int) -> str:
        src = self.master.ptr
        self.master.execute_command(f"CPY APX")
        self.master.execute_command(f"PT APX")
        cmm = "+"*num
        self.master.apply(cmm)
        self.master.execute_command(f"PT {src}")
        return ""


class ADDV(Command):
    name = "ADDV"
    args_count = 1

    def eval(self, adder: Union[str, int]) -> int:
        src = self.master.ptr
        self.master.execute_command(f"CPY APX")
        self.master.execute_command(f"PT {adder}")
        self.master.execute_command(f"CPY APX")
        self.master.execute_command(f"PT {src}")
        return ""


class SUBN(Command):
    name = "SUBN"
    args_count = 1

    def eval(self, num: int) -> str:
        src = self.master.ptr
        self.master.execute_command(f"CPY APX")
        self.master.execute_command(f"PT APX")
        cmm = "-"*num
        self.master.apply(cmm)
        self.master.execute_command(f"PT {src}")
        return ""


class SUBV(Command):
    name = "SUBN"
    args_count = 1

    def eval(self, by) -> str:
        src = self.master.ptr
        self.master.execute_command("CPY APX")
        self.master.execute_command("PT {src}")
        self.master.execute_command("CPY BPX")
        self.master.execute_command("PT BPX")

        sign, dist, _ = self.master.memdir(self.master.ptr, "APX")
        command = f"[-{sign*dist}-{anti_sign(sign)*dist}]"

        return command


class RAPX(Command):
    name = "RAPX"
    args_count = 0

    def eval(self) -> str:
        src = self.master.ptr
        self.master.execute_command("PT APX")
        self.master.execute_command("RST")
        self.master.execute_command(f"PT {src}")
        return ""


class RCBAR(Command):
    name = "RBR"
    args_count = 1

    def eval(self, by) -> str:
        src = self.master.ptr
        self.master.execute_command("PT CBAR")
        self.master.execute_command("RST")
        self.master.execute_command(f"PT {src}")
        return ""


class SETN(Command):
    name = "SETN"
    args_count = 1

    def eval(self, num: int) -> str:
        self.master.execute_command("RST")
        num = int(num)
        sign = "+" if num >= 0 else "-"
        cmm = sign*abs(num)
        return cmm


class AIFSTART(Command):
    name = "AIFSTART"
    args_count = 0

    def eval(self) -> str:
        mark = self.master.ptr
        self.master.execute_command("PT IFA")
        self.master.apply("[")
        self.master.apply("[-]")
        self.master.execute_command(f"PT {mark}")
        return ""


class AIFEND(Command):
    name = "AIFEND"
    args_count = 0

    def eval(self) -> str:
        mark = self.master.ptr
        self.master.execute_command("PT ZERO")
        self.master.apply("]")
        self.master.execute_command(f"PT {mark}")
        return ""


class AEQ(Command):
    name = "EQA"
    args_count = 0

    def eval(self) -> str:
        ptr = self.master.ptr
        self.master.execute_command("PT APX")
        self.master.execute_command("CPY DBAR")
        self.master.execute_command("PT ACMPA")
        self.master.execute_command("SUBV ACMPB")
        self.master.execute_command("PT APX")
        self.master.apply("[")
        self.master.execute_command("PT ACMPC")
        self.master.apply("[-]+")
        self.master.execute_command("PT ZERO")
        self.master.apply("]")
        self.master.execute_command("PT DBAR")
        self.master.execute_command("MOV APX")
        self.master.execute_command(f"PT {ptr}")
        return ""


class CLTZERO(Command):
    name = "CLTZERO"
    args_count = 0

    def eval(self):
        pass


class IFZERO(Command):
    name = "IFZERO"
    args_count = 0

    def eval(self):
        base = self.master.ptr
        self.master.execute_command("PT ACMPA")
        self.master.apply("[[->+<]>>-<<]>>+<[-<+>]<[-]")
        self.master.execute_command(f"PT {base}")
        return ""


class IFSTART(Command):
    name = "IFSTART"
    args_count = 0

    def eval(self):
        base = self.master.ptr
        self.master.base = base
        self.master.execute_command("PT ACMPA")
        self.master.apply("[[-]")
        self.master.execute_command(f"PT {base}")
        self.master.apply("V")
        self.master.execute_command(f"PT ACMPA")
        self.master.apply("M")
        self.master.apply("]")
        self.master.ptr = base
        return


class IFEND(Command):
    name = "IFEND"
    args_count = 0

    def after_e(self):
        pos_start = self.master._command.find("M")+1
        return self.master._command[pos_start+1:],pos_start-1

    def eval(self):
        if_command,m_pos = self.after_e()

        removed = remove_nested_square_brackets(if_command)
        distance = removed.count(">")-removed.count("<")

        sign = ">"
        if distance < 0:
            sign = "<"

        distance = abs(distance)
        extension = sign*distance

        self.master._command = self.master._command[:m_pos]

        self.master.apply(f"{extension}]")
        self.master._command = self.master._command.replace("V",if_command)


        self.master.ptr = self.master.get_memory_location("ACMPA")
        self.master.execute_command(f"PT {self.master.base}")
        return ""