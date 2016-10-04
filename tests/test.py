# -*- coding: utf-8 -*-

from greenbuttonrest.client import GreenClient


def main():
    gc = GreenClient()
    # execute = gc.execute("authorization")
    # execute = gc.execute("interval_block", 1)
    execute = gc.execute("application_information")
    # execute = gc.execute("application_information", 1, published_max="Hello world")
    # execute = gc.execute("application_information")
    # execute = gc.execute("batch_bulk", 1)

    # execute = gc.execute("batch_subscription", 3)
    print(execute)


if __name__ == '__main__':
    main()
