from brainf import BrainF,opti_brain


d = BrainF(5)
d.execute_command("INPUT")
d.execute_command("PT IX")
d.execute_command("MOV 0")
d.execute_command("INPUT")
d.execute_command("PT IX")
d.execute_command("MOV 1")
d.execute_command("PT 0")
d.execute_command("ADDV 1")
d.execute_command("OUTPUT")
print(d.command)
# print(d.memory)