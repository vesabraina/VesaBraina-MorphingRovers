import os, subprocess, sys

def pergatit_esa():
    """Shkarkon kodin e ESA-s dhe bën 2 rregullimet. Thirret 1 herë në fillim."""
    os.chdir("/kaggle/working")
    if not os.path.exists("SpOC2"):
        subprocess.run("git clone -q https://github.com/esa/SpOC2.git", shell=True)
    os.chdir("/kaggle/working/SpOC2/Morphing Rovers")

    # kopjo hartat aty ku i kërkon kodi
    subprocess.run("mkdir -p data/spoc2/morphing && cp -r data/Maps data/coordinates.txt "
                   "data/example_rover.npy data/spoc2/morphing/", shell=True)

    # 2 rregullimet (njëlloj si sed)
    with open("morphing_udp.py") as f:
        rreshtat = f.readlines()
    rreshtat[76] = "HEIGHTMAP_NAMES = ['Map1.jpg', 'Map2.jpg', 'Map3.jpg', 'Map4.jpg', 'Map5.jpg', 'Map6.jpg']\n"
    rreshtat[682] = rreshtat[682].replace(", angle,", ", float(angle),")
    with open("morphing_udp.py", "w") as f:
        f.writelines(rreshtat)

    subprocess.run("pip install -q cma", shell=True)
    sys.path.append(os.getcwd())
    print("ESA gati ✅")
