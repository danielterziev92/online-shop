import time
from typing import Dict, Any

import redis
import requests
from django.db import connection
from django.utils import timezone
from ninja_extra import api_controller, http_get
from pydantic.dataclasses import dataclass
from requests import RequestException

from server import settings


@dataclass
class HealthSchema:
    status: str
    database: str
    cache: str
    loki: str
    grafana: str
    timestamp: str
    response_time_ms: int
    services: Dict[str, Any]


@api_controller("/health", tags=["health"])
class HealthController:

    @http_get("", response=HealthSchema, summary="Health check")
    def health_check(self) -> HealthSchema:
        """Health check endpoint for a system"""
        start_time = time.time()

        db_status = self._check_database()
        cache_status = self._check_redis()
        loki_status = self._check_loki()
        grafana_status = self._check_grafana()

        response_time = int((time.time() - start_time) * 1000)

        overall_status = "ok" if all([
            db_status["status"] == "ok",
            cache_status["status"] == "ok",
            loki_status["status"] == "ok",
            grafana_status["status"] == "ok"
        ]) else "degraded"

        services_detail = {
            "database": db_status,
            "cache": cache_status,
            "loki": loki_status,
            "grafana": grafana_status
        }

        current_time = timezone.now()
        timestamp = current_time.isoformat() + "Z"

        return HealthSchema(
            status=overall_status,
            database=db_status["status"],
            cache=cache_status["status"],
            loki=loki_status["status"],
            grafana=grafana_status["status"],
            timestamp=timestamp,
            response_time_ms=response_time,
            services=services_detail
        )

    @staticmethod
    def _check_database() -> Dict[str, Any]:
        """Check PostgresSQL database connection"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return {
                    "status": "ok",
                    "message": "Database connection successful",
                    "details": {"type": "PostgreSQL"}
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Database connection failed: {str(e)}",
                "details": {"type": "PostgreSQL", "error": str(e)}
            }

    @staticmethod
    def _check_redis() -> Dict[str, Any]:
        """Check Redis cache connection"""
        try:
            redis_client = redis.Redis(
                host=getattr(settings, "REDIS_HOST", "redis"),
                port=getattr(settings, "REDIS_PORT", 6379),
                db=getattr(settings, "REDIS_DB", 0),
                socket_timeout=5
            )

            redis_client.ping()

            return {
                "status": "ok",
                "message": "Redis connection successful",
                "details": {"type": "Redis"}
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Redis connection failed: {str(e)}",
                "details": {"type": "Redis", "error": str(e)}
            }

    @staticmethod
    def _check_loki() -> Dict[str, Any]:
        """Check Loki service"""
        try:
            loki_url = getattr(settings, 'LOKI_URL', 'http://loki:3100')
            response = requests.get(f"{loki_url}/ready", timeout=5)

            if response.status_code == 200:
                return {
                    "status": "ok",
                    "message": "Loki service is ready",
                    "details": {"type": "Loki", "url": loki_url}
                }
            else:
                return {
                    "status": "error",
                    "message": f"Loki service returned status {response.status_code}",
                    "details": {"type": "Loki", "url": loki_url, "status_code": response.status_code}
                }
        except RequestException as e:
            return {
                "status": "error",
                "message": f"Loki service check failed: {str(e)}",
                "details": {"type": "Loki", "error": str(e)}
            }

    @staticmethod
    def _check_grafana() -> Dict[str, Any]:
        """Check Grafana service"""
        try:
            grafana_url = getattr(settings, 'GRAFANA_URL', 'http://grafana:3000')
            response = requests.get(f"{grafana_url}/api/health", timeout=5)

            if response.status_code == 200:
                return {
                    "status": "ok",
                    "message": "Grafana service is healthy",
                    "details": {"type": "Grafana", "url": grafana_url}
                }
            else:
                return {
                    "status": "error",
                    "message": f"Grafana service returned status {response.status_code}",
                    "details": {"type": "Grafana", "url": grafana_url, "status_code": response.status_code}
                }
        except RequestException as e:
            return {
                "status": "error",
                "message": f"Grafana service check failed: {str(e)}",
                "details": {"type": "Grafana", "error": str(e)}
            }
