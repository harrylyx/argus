from typing import Any

class Pipeline:
    async def process(self, data: Any, source_name: str):
        """
        Standardized pipeline: Validator -> Cleaner -> Deduplicator -> Storage
        """
        print(f"[{source_name}] Pipeline received data: {data}")
        # Mocking the steps
        # 1. Validate
        # 2. Clean
        # 3. Deduplicate
        # 4. Store (Postgres/Redis)
        print(f"[{source_name}] Data stored successfully.")

pipeline = Pipeline()
