from enum import Enum


class UploadSessionStatus(str, Enum):
    """Status of an upload session"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"


class StatementType(str, Enum):
    """Type of financial statement"""
    CAMS = "cams"
    KFINTECH = "kfintech"
    ZERODHA = "zerodha"
    PMS = "pms"
    AIF = "aif"
    MANUAL = "manual"


class TransactionType(str, Enum):
    """Type of financial transaction"""
    PURCHASE = "purchase"
    SALE = "sale"
    DIVIDEND = "dividend"
    INTEREST = "interest"
    REDEMPTION = "redemption"
    SWITCH = "switch"
    SIP = "sip"
    STP = "stp"
    SWP = "swp"
    BONUS = "bonus"
    SPLIT = "split"
    OTHER = "other"
