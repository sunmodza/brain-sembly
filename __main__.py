from brainf import BrainF,opti_brain


d = BrainF(5)
d.execute_command("PT BCMPA")
d.apply("+>++<")
d.execute_command("GT")

print(d.command)
# print(d.memory)