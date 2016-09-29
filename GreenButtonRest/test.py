from GreenButtonRest.clientV2 import GreenClient


def main():
    gc = GreenClient()
    execute = gc.execute("ApplicationInformation")
    print(execute.text)


if __name__ == '__main__':
    main()
