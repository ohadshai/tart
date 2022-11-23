import logging
import coloredlogs
import verboselogs
import sys

SUCCESS = 12


def _replace_log_level():
    delattr(logging, 'SUCCESS')
    verboselogs.SUCCESS = SUCCESS
    verboselogs.add_log_level(SUCCESS, 'SUCCESS')


def disable_other_loggers():
    logging.getLogger().disabled = True
    logging.getLogger('pymobiledevice3.lockdown').disabled = True
    logging.getLogger('pymobiledevice3.services.installation_proxy').disabled = True
    logging.getLogger('pymobiledevice3.tcp_forwarder').disabled = True
    logging.getLogger('paramiko.transport').disabled = True
    logging.getLogger('paramiko.transport.sftp').disabled = True
    logging.getLogger('urllib3.connectionpool').disabled = True
    logging.getLogger('asyncio').disabled = True


def configure_logger(name='Tart', level='debug'):
    # from tart.config.config import get_config
    # config = get_config()
    # level = logging._nameToLevel[level and level.upper or config.log.level.upper()]
    level = logging._nameToLevel[level and level.upper()]
    # disable_other_loggers()
    _replace_log_level()

    verboselogs.install()
    logger = logging.getLogger(name=name)
    logger.propagate = False
    fmt = "[%(asctime)s] - %(levelname)s - %(module)s:%(funcName)s - %(message)s"

    coloredlogs.install(level=level, logger=logger, fmt=fmt, stream=sys.stdout)


def get_logger(name='Tart'):
    return logging.getLogger(name=name)
