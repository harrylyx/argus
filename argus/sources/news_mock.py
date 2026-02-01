import asyncio
import time
from typing import Any, Callable
from argus.core.base import BaseSource, HealthStatus

class MockNewsSource(BaseSource):
    name = "Mock News Feed"
    description = "Generates random news headlines."

    async def run(self, pipeline_callback: Callable[[Any], None]):
        headlines = [
            "Bitcoin reaches new all-time high",
            "Fed announces interest rate hike",
            "Tech stocks rally on earnings",
            "New AI model released by Google"
        ]
        import random
        while self.is_active:
            news = {
                "title": random.choice(headlines),
                "source": "MockNews",
                "published_at": time.time()
            }
            await pipeline_callback(news)
            await asyncio.sleep(10)

    async def check_health(self) -> HealthStatus:
        start = time.time()
        await asyncio.sleep(0.05)
        return HealthStatus(
            is_healthy=True,
            latency_ms=(time.time() - start) * 1000,
            last_success_time=str(time.time())
        )

    async def dry_run(self) -> Any:
        return {
            "title": "Dry Run: Market Crash Imminent?",
            "source": "MockNews",
            "published_at": time.time()
        }
