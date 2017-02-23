import sys
def main():
    with open(sys.argv[1]) as f:
        lines = f.readlines()
        videos, endpoints, request_descriptions, caches, size = map(int, lines[0].split())

if __name__ == "__main__":
    main()
