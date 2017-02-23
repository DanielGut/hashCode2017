import sys
import operator
from collections import defaultdict

class Endpoint(object):
    def __init__(self):
        self.data_latency = None
        self.cache_latency = {}

    def get_sorted_cache(self):
        return sorted(self.cache_latency.iteritems(), key=operator.itemgetter(1))


class Requests(object):
    def __init__(self, endpoint, count):
        self.endpoint = endpoint
        self.request_count = count


class Video(object):
    def __init__(self, idx, size):
        self.idx = idx
        self.size = size
        self.requests = []


def main():
    endpoints = []
    videos = []
    cache_to_endpoint_map = defaultdict(set)

    with open(sys.argv[1]) as f:
        lines = f.readlines()
        videos_count, endpoints_count, request_descriptions, caches, size = map(int, lines[0].split())
        for idx, video_size in enumerate(map(int, lines[1].split())):
            videos.append(Video(idx, video_size))

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


    videos = sorted(videos, key=lambda x: x.size)

    class Cache(object):
        def __init__(self):
            self.size = size
            self.videos = set()

    used_caches = defaultdict(Cache)
    for video in videos:
        for req in sorted(video.requests, key=lambda x: x.request_count)[::-1]:
            e = endpoints[req.endpoint]
            if e.cache_latency:
                caches = e.get_sorted_cache()
                for cache in caches:
                    cache = used_caches[cache[0]]
                    if cache.size - video.size >= 0:
                        cache.size -= video.size
                        cache.videos.add(video.idx)
                        break

    count = 0
    lines = []
    for idx, cache in used_caches.iteritems():
        if cache.videos:
            lines.append(str(idx) + " " + " ".join(map(str, cache.videos)))
            count += 1
    print count
    for line in lines:
        print line

if __name__ == "__main__":
    main()
