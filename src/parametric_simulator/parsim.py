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
    """
    Parse command-line arguments for the ParametricSimulator script.

    Returns:
        argparse.Namespace: Parsed command-line arguments containing:
            - 'version': Display the current version of ParametricSimulator.
            - 'script': Path to the script to execute, or obtained from settings if not provided.
            - 'settings_file': Path to the settings file with processing information.
            - 'loglevel': Logging level, set to INFO with '-v' or DEBUG with '-vv', defaults to WARN.
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
    """
    Main function for the ParametricSimulator script.

    This function is the entry point for the script, utilizing Hydra for configuration management.
    It parses command-line arguments, sets up logging, and reads settings from a specified file.

    Args:
        cfg (ParametricSimulatorConfig): Configuration object provided by Hydra.

    Steps:
        1. Parse command-line arguments to determine the script and settings file paths.
        2. Setup logging based on the specified log level.
        3. If a settings file is provided, read and load the general settings.

    Note:
        The function will exit with an error code if the 'general' section is missing in the settings file.
    """
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
    """
    Main entry point for the ParametricSimulator script.

    This function serves as the entry point for the script, intended to be executed
    as a standalone program. It delegates the execution to the `main` function, which
    handles the argument parsing, logging setup, and script execution.

    Returns:
        None
    """
    main()


if __name__ == "__main__":
    run()
