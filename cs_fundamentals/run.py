import uvicorn
from cs_fundamentals.core.logging_config import setup_logging

if __name__ == "__main__":
    log_config = setup_logging("cs_fundamentals")
    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_config=log_config,  # Unified logging
        access_log=False,  # RequestLogMiddleware handles it
    )
