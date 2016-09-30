from GreenButtonRest.clientV2 import GreenClient


def main():
    gc = GreenClient()
    # execute = gc.execute("application_information")
    # execute = gc.execute("application_information_by_id", 1)
    # execute = gc.execute("application_information")
    execute = gc.execute("batch_bulk", 1)
    print(execute.text)


if __name__ == '__main__':
    main()
