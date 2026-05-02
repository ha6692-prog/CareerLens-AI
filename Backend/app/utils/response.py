# ============================================================
# utils/response.py — Standard API Response Format
# ============================================================
# Keeps all API responses in a consistent shape so the
# frontend always knows what to expect.
#
# Success: { "success": true,  "data": {...} }
# Error:   { "success": false, "error": "message" }
# ============================================================

from typing import Any


def success_response(data: Any, message: str = "Success") -> dict:
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(message: str) -> dict:
    return {
        "success": False,
        "message": message,
        "data": None,
    }