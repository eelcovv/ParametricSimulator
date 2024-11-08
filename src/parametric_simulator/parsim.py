"""
A simple Python script to run a script with a set of parameters.
"""

import argparse
import logging
import sys
from pathlib import Path

import hydra
import yaml
from hydra.core.config_store import ConfigStore

from parametric_simulator import __version__
from parametric_simulator.config import ParametricSimulatorConfig

__author__ = "Eelco van Vliet"
__copyright__ = "Eelco van Vliet"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

CONFDIR = Path(__file__).parent / Path("conf")


def parse_args():
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example, ``["--help"]``).

    Returns:
      obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")
    parser.add_argument(
        "--version",
        action="version",
        version=f"ParametricSimulator {__version__}",
    )
    parser.add_argument(
        "--script",
        help="The script to execute. If not given"
        ", the script will be obtained from the settings file.",
    )
    parser.add_argument(
        "--settings_file",
        help="The settings file containing with all the processing information",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    parsed_arguments = parser.parse_args()
    parsed_arguments.loglevel = parsed_arguments.loglevel or logging.WARN
    return parsed_arguments


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    log_format = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel,
        stream=sys.stdout,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


cs = ConfigStore.instance()
cs.store(name="parametric_simulator_config", node=ParametricSimulatorConfig)


@hydra.main(version_base=None, config_path=CONFDIR.as_posix(), config_name="config")
def main(cfg: ParametricSimulatorConfig):
    print(cfg)
    print(cfg.general.max_workers)
    return
    args = parse_args()
    setup_logging(args.loglevel)

    general_settings = None

    if args.settings_file is not None:
        _logger.info(f"Reading settings file: {args.settings_file}")
        with open(args.settings_file) as stream:
            settings = yaml.safe_load(stream)
        try:
            general_settings = settings["general"]
        except KeyError as err:
            _logger.error(f"KeyError: {err}")
            _logger.error("Could not find 'general' in settings file. Exiting.")
            sys.exit(1)

    print(general_settings)


def run():
    main()


if __name__ == "__main__":
    run()
