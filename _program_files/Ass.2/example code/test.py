import subprocess

for i in range(25):
    ok=True
    while ok:
        ok=False
        try:
            r = subprocess.run([r'E:\User Applications\Software\Miniconda3\envs\SpikingJelly\python.exe',
                                r'E:\User Applications\App Files\Projects\SBU-CS-22_AI\_program_files\Ass.2\example code\generate_problem.py', '0'], timeout=5)
        except:
            ok=True