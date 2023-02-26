class MemoryUnit:
    value: int = 0

    def __init__(self, location: int = -1) -> None:
        self.location = location


class Register(MemoryUnit):
    name: str
    value: int = 0

    def __init__(self) -> None:
        self.location = None
        super().__init__()


class PX(Register):
    name = "PX"


class AX(Register):
    name = "AX"


class BX(Register):
    name = "BX"


class CX(Register):
    name = "CX"


class DX(Register):
    name = "DX"


class CBAR(Register):
    name = "CBAR"


class IX(Register):
    name = "IX"


class APX(Register):
    name = "APX"


class BPX(Register):
    name = "BPX"


class CPX(Register):
    name = "CPX"


class DPX(Register):
    name = "DPX"


class IFA(Register):
    name = "IFA"


class ZERO(Register):
    name = "ZERO"


class ACMPA(Register):
    name = "ACMPA"


class ACMPB(Register):
    name = "ACMPB"


class ACMPC(Register):
    name = "ACMPC"

class ACMPD(Register):
    name = "ACMPD"


class IFZ(Register):
    name = "IFZ"
