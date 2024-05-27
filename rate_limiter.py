import redis
import time
import logging

from flask import Flask, jsonify, request

logging.basicConfig(level=logging.DEBUG)

RATE_LIMIT = 'rate_limit'
INTERVAL = 'interval'

app = Flask(__name__)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


@app.route('/api/configure', methods=['POST'])
def configure():
    # Extract interval and rate limit from request JSON
    # TO-DO: validate data format, range
    data = request.json
    interval = data.get(INTERVAL)
    rate_limit = data.get(RATE_LIMIT)

    try:
        redis_client.set(INTERVAL, interval)
        redis_client.set(RATE_LIMIT, rate_limit)
    except Exception as e:
        logging.error(f"Error setting interval={interval} and rate_limit={rate_limit} to Redis: {e}")
        return jsonify({'error': 'Failed to configure interval and rate limit'}), 500

    # Response with successful message
    return jsonify({'message': 'Interval and Rate limit configured successfully'}), 200


@app.route('/api/is_rate_limited/<unique_token>', methods=['GET'])
def is_rate_limited(unique_token):
    # Retrieve interval and rate limit from Redis
    interval = int(redis_client.get(INTERVAL))
    rate_limit = int(redis_client.get(RATE_LIMIT))

    logging.debug(f"interval={interval}, rate_limit={rate_limit}")

    # Calculate window index and append to unique_token as key
    current_timestamp = int(time.time())
    window_index = current_timestamp // interval
    key = f"{unique_token}:{window_index}"

    # Increment counter for the key, set expiration time, and get total requests
    redis_client.hincrby('counters', key, 1)
    redis_client.expire(key, interval)
    total_requests = int(redis_client.hget('counters', key))

    logging.debug(f"key={key}, total_requests={total_requests}")

    # Respond with rate limiting status
    return jsonify({'is_rate_limited': total_requests > rate_limit}), 200


if __name__ == '__main__':
    app.run(debug=True)
