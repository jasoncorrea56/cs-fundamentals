from monkeytype.config import DefaultConfig


class Config(DefaultConfig):
    def trace_modules(self) -> set[str]:
        return {"cs_fundamentals", "automation"}


CONFIG = Config()
