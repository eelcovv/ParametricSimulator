"""
A simple Python script to run a script with a set of parameters.
"""

import argparse
import logging
import sys
from pathlib import Path

import hydra
import yaml

from parametric_simulator import __version__

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


@hydra.main(version_base=None, config_path=CONFDIR.as_posix(), config_name="config")
def main(cfg):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      cfg:
      args (List[str]): command line parameters as a list of strings
          (for example, ``["--verbose", "42"]``).
    """
    print(cfg)
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
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as an entry point to create console scripts with setuptools.
    """
    main()


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m parametric_simulator.skeleton 42
    #
    run()
