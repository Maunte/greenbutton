from GreenButtonRest.client import GreenClient


def main():
    gc = GreenClient()
    # execute = gc.execute("authorization")
    # execute = gc.execute("interval_block", 1)
    # execute = gc.execute("application_information", 1)
    execute = gc.execute("application_information_by_id", 1)
    # execute = gc.execute("application_information")
    # execute = gc.execute("batch_bulk", 1)
    print(execute)
    print(gc.API_CALLS_MADE)


if __name__ == '__main__':
    main()
