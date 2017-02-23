import sys
from collections import defaultdict

class Endpoint(object):
    def __init__(self):
        self.data_latency = None
        self.cache_latency = {}


class Requests(object):
    def __init__(self, endpoint, count):
        self.endpoint = endpoint
        self.request_count = count


class Video(object):
    def __init__(self, size):
        self.size = size
        self.requests = []


def main():
    endpoints = []
    videos = []
    cache_to_endpoint_map = defaultdict(set)

    with open(sys.argv[1]) as f:
        lines = f.readlines()
        videos_count, endpoints_count, request_descriptions, caches, size = map(int, lines[0].split())
        for video_size in map(int, lines[1].split()):
            videos.append(Video(video_size))

        current_line = 2
        for endpoint_id in range(endpoints_count):
            line = map(int, lines[current_line].split())
            e = Endpoint()
            e.data_latency = line[0]
            caches_count = line[1]
            current_line += 1
            for j in range(caches_count):
                cache_id, latency = map(int, lines[current_line].split())
                cache_to_endpoint_map[cache_id].add(endpoint_id)
                e.cache_latency[cache_id] = latency
                current_line += 1
            endpoints.append(e)

        for line in lines[current_line:]:
            video_idx, endpoint_idx, requests = map(int, line.split())
            videos[video_idx].requests.append(Requests(endpoint_idx, requests))

if __name__ == "__main__":
    main()
