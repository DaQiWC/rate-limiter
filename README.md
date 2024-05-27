# Rate Limiter Microservice

This microservice implements a configurable rate limiter through a REST API. It allows clients to configure the rate limit interval and the number of calls allowed per interval. The service exposes two REST endpoints:

1. `POST /api/configure`: Allows the caller to change the interval of rate limiting (in seconds) as well as the number of calls allowed per interval. 
   
2. `GET /api/is_rate_limited/<unique_token>`: Returns the status of rate limiting for the specified unique token. It checks if the rate limit for the unique token has been exceeded based on the configured interval and rate limit.

## Setup

### Installation

1. Clone the repository:

```bash
git clone https://github.com/DaQiWC/rate-limiter.git
```

2. Install virtual environment

```bash
python3 -m venv myenv
source myenv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Ensure Redis is installed and running on `localhost` with default port `6379`.

```bash
brew install redis
brew services start redis
```


## Usage

1. Run the Rate Limiter:

```bash
python rate_limiter.py
```

2. Run the unit tests:
```bash
python test_rate_limiter.py
```

## Endpoints

### `POST /api/configure`

Allows configuring the rate limit interval and the number of calls allowed per interval.

- Request body:

```json
{
  "interval": 30,
  "rate_limit": 2
}
```

- Example:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"interval": 30, "rate_limit": 2}' http://localhost:5000/api/configure
```

### `GET /api/is_rate_limited/<unique_token>`

Returns the status of rate limiting for the specified unique token.

- Example:

```bash
curl http://localhost:5000/api/is_rate_limited/123
```
