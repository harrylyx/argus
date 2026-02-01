from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Optional, Any, Callable

class HealthStatus(BaseModel):
    is_healthy: bool
    latency_ms: float
    last_error: Optional[str] = None
    last_success_time: Optional[str] = None

class BaseSource(ABC):
    # 1. 元数据：在UI上显示的名字、描述、图标
    name: str = "Generic Source"
    description: str = "Base description"
    is_active: bool = True # 控制开关
    
    # 2. 核心：抓取逻辑 (生产环境跑这个)
    @abstractmethod
    async def run(self, pipeline_callback: Callable[[Any], None]):
        """主循环：一直运行或定时运行"""
        pass

    # 3. 核心：体检逻辑 (UI监控跑这个)
    @abstractmethod
    async def check_health(self) -> HealthStatus:
        """
        轻量级测试。不要抓取大量数据，
        只要 ping 通 API 或 抓取 1 条数据验证格式即可。
        """
        pass
    
    # 4. 调试：测试运行 (开发时跑这个)
    @abstractmethod
    async def dry_run(self) -> Any:
        """抓取一次并打印结果，不入库，方便你在 UI 上点击 'Test' 按钮调试"""
        pass
