import subprocess

for i in range(25):
    print('trying for problem', i)
    ok=True
    while ok:
        ok=False
        try:
            r = subprocess.run([r'E:\User Applications\Software\Miniconda3\envs\SpikingJelly\python.exe',
                                r'E:\User Applications\App Files\Projects\SBU-CS-22_AI\_program_files\Ass.2\example code\Generator_methods.py', str(i)], timeout=7)
            if r.returncode!=0: raise Exception
        except:
            ok=True