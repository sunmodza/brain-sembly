from brainf import BrainF,opti_brain


d = BrainF(5)
d.execute_command("PT ACMPA")
d.apply("+")
d.execute_command("PT 0")
d.execute_command("IFSTART")
d.apply("+")
d.execute_command("IFEND")
print(d.command)
# print(d.memory)