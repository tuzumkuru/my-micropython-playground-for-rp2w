import mip

def install_packages():
    with open("requirements.txt", "r") as f:
        for line in f:
            package = line.strip()
            if package:
                print(f"Installing {package}...")
                try:
                    mip.install(package)
                except Exception as e:
                    print(f"Error installing {package}: {e}")

install_packages()
