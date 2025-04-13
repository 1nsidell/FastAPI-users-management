from ..health_check.liveness import (
    router as liveness_router,
)
from ..health_check.readiness import (
    router as readiness_router,
)

__all__ = ["liveness_router", "readiness_router"]
