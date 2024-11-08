"""
This is a simple script that sleeps for a certain amount of time.

Examples

Sleep for 10 seconds::

    python sleeping.py --sleep 10

Sleep for 0.1 minute::

    python sleeping.py --sleep 0.1 --units m
"""

import argparse
import logging
import sys
from time import sleep

UNITS = {"s": 1, "m": 60, "h": 3600}

_logger = logging.getLogger(__name__)


def parse_the_arguments(argv):
    """
    Parse command-line arguments for the sleeping script.

    Args:
        argv (List[str]): Command-line arguments as a list of strings.

    Returns:
        argparse.Namespace: Parsed command-line arguments containing
        'sleep', 'units', and 'loglevel'.
    """
    # Create argument parser with description and default help formatter
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Run a python process and wait for a certain sleeping time",
    )

    # Add sleep time argument
    parser.add_argument("-s", "--sleep", type=float, default=1, help="How long to sleep")

    # Add time units argument with choices from UNITS
    parser.add_argument(
        "-u",
        "--units",
        default="s",
        help="Units of time. Must be one of {}".format(list(UNITS.keys())),
        choices=list(UNITS.keys()),
    )

    # Add verbosity level arguments for logging
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="Set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--debug",
        dest="loglevel",
        help="Set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )

    # Parse the arguments and return
    args = parser.parse_args(args=argv)
    return args


def setup_logging(loglevel):
    """
    Set up basic logging configuration.

    This function sets up a simple configuration for Python's built-in
    logging module. The logging level is set to the provided `loglevel`
    argument, and the log messages are formatted as follows:

    .. code-block:: text

        [%(asctime)s] %(levelname)s:%(name)s:%(message)s

    Where:

    - %(asctime)s: The time of the log message, formatted as
      ``YYYY-MM-DD HH:MM:SS``.
    - %(levelname)s: The log level (e.g., ``INFO``, ``WARNING``, etc.).
    - %(name)s: The name of the logger (often the module name).
    - %(message)s: The log message itself.

    Args:
        loglevel (int): The minimum log level for emitting messages.
    """
    log_format = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel,
        stream=sys.stdout,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def get_number_of_seconds(sleep_time: float, units: str) -> int:
    """
    Convert sleep time into seconds.

    This function takes a sleep time and a unit of time, then calculates
    the equivalent number of seconds.

    Args:
      sleep_time (float): The amount of time to sleep.
      units (str): The unit of time.
         This can be 's' for seconds, 'm' for minutes, or 'h' for hours.

    Returns:
      int: The equivalent amount of time in seconds.

    Raises:
      KeyError: If the provided unit is not in the UNITS dictionary.
    """
    # Log the conversion operation at debug level
    _logger.debug(f"Converting argument {sleep_time} and {units} into seconds")

    # Convert the sleep time into seconds using the UNITS dictionary
    return sleep_time * UNITS[units]


def main(argv):
    """
    Main function for the sleeping script.

    This function parses the command-line arguments, sets up logging,
    calculates the number of seconds to sleep, and then performs the sleep operation.

    Args:
        argv (List[str]): Command-line arguments as a list of strings.
    """
    # Parse command-line arguments
    args = parse_the_arguments(argv)

    # Set up logging
    setup_logging(args.loglevel)

    # Calculate the number of seconds to wait
    number_of_seconds_to_wait = get_number_of_seconds(sleep_time=args.sleep, units=args.units)

    # Log the start of the sleep script and sleep operation
    _logger.info(f"Start dummy script here. Going to sleep for {number_of_seconds_to_wait} seconds")

    # Sleep for the calculated number of seconds
    sleep(number_of_seconds_to_wait)

    # Log the completion of the sleep operation
    _logger.info("Done with sleep")


def run():
    """
    Main entry point for the sleeping script.

    This function serves as the entry point for the script, intended to be executed
    as a standalone program. It delegates the execution to the `main` function, which
    handles the argument parsing, logging setup, and sleep operation.

    Returns:
        None
    """
    # Delegate to the main function with command-line arguments
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
