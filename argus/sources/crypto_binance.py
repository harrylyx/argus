import asyncio
import random
import time
from typing import Any, Callable
from argus.core.base import BaseSource, HealthStatus

class BinanceSource(BaseSource):
    name = "Binance Crypto Ticker"
    description = "Fetches BTC/USDT price from Binance mock."
    
    async def run(self, pipeline_callback: Callable[[Any], None]):
        while self.is_active:
            # Simulate fetching data
            price = 50000 + random.uniform(-100, 100)
            data = {"symbol": "BTCUSDT", "price": price, "timestamp": time.time()}
            await pipeline_callback(data)
            await asyncio.sleep(5) # Fetch every 5 seconds

    async def check_health(self) -> HealthStatus:
        # Simulate a health check
        start = time.time()
        # Pretend we pinged Binance
        await asyncio.sleep(0.1) 
        latency = (time.time() - start) * 1000
        
        return HealthStatus(
            is_healthy=True,
            latency_ms=latency,
            last_success_time=str(time.time())
        )

    async def dry_run(self) -> Any:
        return {"symbol": "BTCUSDT", "price": 50123.45, "timestamp": time.time(), "note": "Dry run data"}
