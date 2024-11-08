import argparse
import logging
import sys
from time import sleep

UNITS = {"s": 1, "m": 60, "h": 3600}

_logger = logging.getLogger(__name__)


def parse_the_arguments(argv):
    """
    Parse command-line arguments for the sleeping script.

    Returns:
        argparse.Namespace: Parsed command-line arguments containing 'sleep' and 'units'.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Run a python process and wait for a certain sleeping time",
    )
    parser.add_argument("-s", "--sleep", type=float, default=1, help="How long to sleep")
    parser.add_argument(
        "-u",
        "--units",
        default="s",
        help="Units of time. Must be one of {}¨".format(list(UNITS.keys())),
        choices=list(UNITS.keys()),
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

    args = parser.parse_args(args=argv)
    return args


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


def get_number_of_seconds(sleep_time: float, units: str) -> int:
    """
    Convert sleep time into seconds.

    Args:
      sleep_time (int): The amount of time to sleep.
      units (str): The unit of time, can be 's' for seconds, 'm' for minutes, or 'h' for hours.

    Returns:
      int: The equivalent amount of time in seconds.
    """
    _logger.debug(f"Converting argument {sleep_time} and {units} in to seconds")
    return sleep_time * UNITS[units]


def main(argv):
    args = parse_the_arguments(argv)
    setup_logging(args.loglevel)

    number_of_seconds_to_wait = get_number_of_seconds(sleep_time=args.sleep, units=args.units)

    _logger.info(f"Start dummy script here. Going to sleep for {number_of_seconds_to_wait} seconds")
    sleep(number_of_seconds_to_wait)
    _logger.info("Done with sleep")


def run():
    """
    Main entry point for the sleeping script.

    Runs the script by calling `parse_the_arguments` and `get_number_of_seconds`
    and then sleep for the specified time.

    Returns:
        None
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
