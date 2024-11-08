import argparse
from time import sleep


def parse_the_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sleep", type=int, default=1, help="How long to sleep in seconds")
    args = parser.parse_args()
    return args


def main():
    args = parse_the_arguments()

    print(f"Start dummy script here. Going to sleep for {args.sleep} seconds")
    sleep(args.sleep)
    print("Done with sleep")


if __name__ == "__main__":
    main()
