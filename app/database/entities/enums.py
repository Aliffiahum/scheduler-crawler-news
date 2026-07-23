from enum import Enum


class NewsStatus(str, Enum):
    RAW = "RAW"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"