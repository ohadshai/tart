import os
import sys
import IPython
from traitlets.config import Config
from colored import style, fore
import uuid

from tart.device import get_device
from tart.__main__ import get_tart
from tart.log import get_logger


logger = get_logger()


def log_env_objects():
    logger.info(f"Environment Objects to use: {style.BOLD}tart, d{style.RESET}\n")


def get_itart_configuration():
    config = Config()
    config.IPCompleter.use_jedi = False
    config.TerminalInteractiveShell.banner2 = f"{fore.BLUE}---------------  Welcome  --------------{style.RESET}\n{fore.LIGHT_YELLOW}INFRA IPython Interpreter - {style.RESET}{style.BOLD}tarte-tatin{style.RESET}\n{fore.BLUE}---------------------------------------{style.RESET}\n\n"

    d = get_device(str(uuid.uuid4()))
    tart = get_tart()

    config.InteractiveShellApp.exec_lines = [
        "from tart.scripts.itart import log_env_objects",
        "log_env_objects()",
        "d.method_1()"
    ]
    itart_path = os.path.expanduser("~/.itart")
    if os.path.exists(itart_path):
        config.InteractiveShellApp.exec_files = itart_path

    ns = globals()
    ns.update(locals())

    return config, ns


def main():
    config, ns = get_itart_configuration()
    sys.exit(IPython.start_ipython(config=config, user_ns=ns))


if __name__ == '__main__':
    main()
