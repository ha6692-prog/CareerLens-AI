# ============================================================
# middleware/logging.py — Request Logger
# ============================================================
# Middleware runs on EVERY request before it hits any route.
# This one logs: method, URL, status code, and how long it took.
# Useful for debugging and monitoring in production.
#
# Example log line:
# POST /auth/login → 200 (142ms)
# ============================================================

import time
import logging
from fastapi import Request

# Standard Python logger — writes to terminal (and log files in production)
logger = logging.getLogger("careerlens")


async def log_requests(request: Request, call_next):
    # Record the time before the request is processed
    start_time = time.time()

    # call_next passes the request to the actual route
    response = await call_next(request)

    # Calculate how long the route took in milliseconds
    duration = (time.time() - start_time) * 1000

    # Log it in a clean format
    logger.info(
        f"{request.method} {request.url.path} → {response.status_code} ({duration:.0f}ms)"
    )

    return response