# utils.py
import os


def get_output_file(input_file):
    output_file = os.path.basename(os.path.splitext(input_file)[0]) + '.out'
    output_file = os.path.join('./output_files', output_file)
    return output_file


def analyze_world(world):
    print("total capacity: %d" % sum(world['caches']))
    print("total video size: %d" % sum(world['videos']))


TOO_BIG_LATENCY = 1000000


def calculate_score(world, solution):
    # first check that cache capacity has not been exceeded
    for cache_id, videos in solution.items():
        size_of_videos_in_cache = sum(world['videos'][video_id] for video_id in videos)
        if size_of_videos_in_cache > world['caches'][cache_id]:
            print("BAD SOLUTION: cache %d contains videos with %d Mb > %d Mb" % (
                cache_id, size_of_videos_in_cache, world['caches'][cache_id])
                  )

    # now, calculate the score
    score = 0
    total_requests = 0
    for request in world['requests']:
        endpoint = world['endpoints'][request['endpoint']]
        caches_containing_video = [cache_id for (cache_id, videos) in solution.items() if request['video'] in videos]
        min_latency = min(
            (endpoint['cache_latency'].get(cache, TOO_BIG_LATENCY) for cache in caches_containing_video),
            default=TOO_BIG_LATENCY
        )
        latency_to_data_center = endpoint['datacenter_latency']

        if min_latency and min_latency < latency_to_data_center:
            time_saved = latency_to_data_center - min_latency
            score += time_saved * request['count']

        total_requests += request['count']

    return score * 1000 / total_requests
