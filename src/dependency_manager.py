import mip
import socket
import time
import sys

def has_internet(host="1.1.1.1", port=80, timeout=3):
    """Quick connectivity check by opening a socket to a public DNS/HTTP host."""
    try:
        addr = socket.getaddrinfo(host, port)[0][-1]
        s = socket.socket()
        s.settimeout(timeout)
        s.connect(addr)
        s.close()
        return True
    except Exception:
        return False

def install_packages(packages=None, requirements_file="requirements.txt", verbose=True):
    """Install packages using mip.

    Args:
        packages (iterable or None): iterable of package names to install. If None, read from requirements_file.
        requirements_file (str): path to requirements file to read when packages is None.
        verbose (bool): whether to print progress messages.

    Returns:
        dict: mapping package name -> True on success or error string on failure.
    """
    result = {}

    if packages is None:
        try:
            with open(requirements_file, "r") as f:
                packages = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
        except Exception as e:
            if verbose:
                print(f"Could not read requirements file '{requirements_file}': {e}")
            return {}

    for package in packages:
        if not package:
            continue
        if verbose:
            print(f"Installing {package}...")
        try:
            mip.install(package)
            result[package] = True
        except Exception as e:
            err = str(e)
            result[package] = err
            if verbose:
                print(f"Error installing {package}: {err}")

    return result


def _normalize_package_name(pkg_str):
    """Turn a requirement-spec (e.g. 'micropython-umqtt.simple==1.3') into a module candidate name.

    Heuristic used to derive an importable module name from a package spec.
    """
    if not pkg_str:
        return None
    for sep in ("==", ">=", "<=", ">", "<", "~="):
        if sep in pkg_str:
            pkg_str = pkg_str.split(sep, 1)[0]
            break
    pkg_str = pkg_str.strip()
    if pkg_str.startswith("micropython-"):
        return pkg_str[len("micropython-"):]
    return pkg_str


def is_package_installed(pkg_str):
    """Return True if importing a likely module for pkg_str succeeds, else False.

    Best-effort check; not perfect for every naming scheme.
    """
    mod = _normalize_package_name(pkg_str)
    if not mod:
        return False
    try:
        __import__(mod)
        return True
    except Exception:
        try:
            __import__(mod.replace('-', '_'))
            return True
        except Exception:
            return False


def check_missing_packages(packages=None, requirements_file="requirements.txt", verbose=True):
    """Return a list of packages that appear missing (need installation).

    Args same as install_packages. Returns a list of requirement strings that are missing.
    """
    if packages is None:
        try:
            with open(requirements_file, "r") as f:
                packages = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
        except Exception as e:
            if verbose:
                print(f"Could not read requirements file '{requirements_file}': {e}")
            return []

    missing = []
    for pkg in packages:
        if not is_package_installed(pkg):
            missing.append(pkg)
        elif verbose:
            print(f"Already present: {pkg}")

    return missing


def install():
    """Run the installer: check connectivity and install requirements."""
    print("Checking internet connectivity...")
    if has_internet():
        print("Internet reachable — installing dependencies.")
        install_packages()
    else:
        print("No internet connection detected. Please connect the device to the internet and run this script again.")
        sys.exit(1)
