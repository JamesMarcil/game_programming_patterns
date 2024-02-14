import sys

if __name__ == "__main__":
    while True:
        try:
            result = input("> ")
            print(result)
        except KeyboardInterrupt:
            sys.exit(0)