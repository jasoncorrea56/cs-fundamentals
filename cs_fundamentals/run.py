import uvicorn
from cs_fundamentals.config import settings
from cs_fundamentals.core.logging_config import setup_logging

if __name__ == "__main__":
    log_config = setup_logging("cs_fundamentals")
    uvicorn.run(
        "cs_fundamentals.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=True,
        log_config=log_config,  # Unified logging
        log_level=settings.log_level.lower(),
        access_log=False,
    )
