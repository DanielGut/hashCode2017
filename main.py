import sys

class Endpoint(object):
    def __init__(self):
        self.data_latency = None
        self.cache_latency = {}

def main():
    with open(sys.argv[1]) as f:
        lines = f.readlines()
        videos, endpoints_count, request_descriptions, caches, size = map(int, lines[0].split())
        videos_sizes = map(int, lines[1].split())
        endpoints = []
        current_line = 2
        for i in range(endpoints_count):
            line = map(int, lines[current_line].split())
            e = Endpoint()
            e.datacenter_latency = line[0]
            caches_count = line[1]
            current_line += 1
            for j in range(caches_count):
                cache_id, latency = map(int, lines[current_line].split())
                e.cache_latency[cache_id] = latency
                current_line += 1
            endpoints.append(e)

if __name__ == "__main__":
    main()
