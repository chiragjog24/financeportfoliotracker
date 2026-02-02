from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlmodel import Field, Relationship, Column, Text, JSON
from sqlalchemy import ForeignKey

from app.db.base import BaseModel
from app.models.enums import UploadSessionStatus, StatementType, TransactionType


class UploadSession(BaseModel, table=True):
    """Tracks the state of a statement upload and parsing session"""
    
    __tablename__ = "upload_sessions"
    
    user_id: str = Field(index=True, nullable=False, description="User ID (UUID)")
    status: UploadSessionStatus = Field(
        default=UploadSessionStatus.PENDING,
        nullable=False,
        description="Current status of the upload session"
    )
    statement_type: Optional[StatementType] = Field(
        default=None,
        nullable=True,
        description="Type of statement being uploaded"
    )
    expires_at: Optional[datetime] = Field(
        default=None,
        nullable=True,
        description="Session expiration timestamp"
    )
    error_message: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
        description="Error message if session failed"
    )
    
    # Relationships
    statements: list["Statement"] = Relationship(back_populates="upload_session")


class Statement(BaseModel, table=True):
    """Represents a financial statement file and its metadata"""
    
    __tablename__ = "statements"
    
    upload_session_id: UUID = Field(
        foreign_key="upload_sessions.id",
        nullable=False,
        index=True,
        description="Reference to the upload session"
    )
    user_id: str = Field(index=True, nullable=False, description="User ID (UUID)")
    file_name: str = Field(nullable=False, description="Original filename")
    file_size_bytes: int = Field(nullable=False, description="File size in bytes")
    statement_type: StatementType = Field(nullable=False, description="Type of statement")
    statement_date: Optional[datetime] = Field(
        default=None,
        nullable=True,
        description="Date of the statement"
    )
    institution_name: Optional[str] = Field(
        default=None,
        nullable=True,
        description="Name of the financial institution"
    )
    folio_number: Optional[str] = Field(
        default=None,
        nullable=True,
        index=True,
        description="Folio number from the statement"
    )
    parsing_confidence: Optional[Decimal] = Field(
        default=None,
        nullable=True,
        description="Confidence score of parsing (0.0 to 1.0)"
    )
    confirmed_at: Optional[datetime] = Field(
        default=None,
        nullable=True,
        description="Timestamp when user confirmed the statement"
    )
    
    # Relationships
    upload_session: UploadSession = Relationship(back_populates="statements")
    parsed_transactions: list["ParsedTransaction"] = Relationship(back_populates="statement")
    statement_file: Optional["StatementFile"] = Relationship(
        back_populates="statement",
        sa_relationship_kwargs={"uselist": False}
    )


class ParsedTransaction(BaseModel, table=True):
    """Represents a transaction parsed from a financial statement"""
    
    __tablename__ = "parsed_transactions"
    
    statement_id: UUID = Field(
        foreign_key="statements.id",
        nullable=False,
        index=True,
        description="Reference to the statement"
    )
    user_id: str = Field(index=True, nullable=False, description="User ID (UUID)")
    transaction_type: TransactionType = Field(nullable=False, description="Type of transaction")
    transaction_date: datetime = Field(nullable=False, index=True, description="Date of transaction")
    security_name: Optional[str] = Field(
        default=None,
        nullable=True,
        description="Name of the security"
    )
    security_symbol: Optional[str] = Field(
        default=None,
        nullable=True,
        index=True,
        description="Symbol/ticker of the security"
    )
    quantity: Optional[Decimal] = Field(
        default=None,
        nullable=True,
        description="Number of units/quantity"
    )
    price_per_unit: Optional[Decimal] = Field(
        default=None,
        nullable=True,
        description="Price per unit"
    )
    nav: Optional[Decimal] = Field(
        default=None,
        nullable=True,
        description="Net Asset Value"
    )
    amount: Optional[Decimal] = Field(
        default=None,
        nullable=True,
        description="Total transaction amount"
    )
    units: Optional[Decimal] = Field(
        default=None,
        nullable=True,
        description="Number of units"
    )
    brokerage_charges: Optional[Decimal] = Field(
        default=None,
        nullable=True,
        description="Brokerage or transaction charges"
    )
    confidence_score: Optional[Decimal] = Field(
        default=None,
        nullable=True,
        description="Confidence score of parsing (0.0 to 1.0)"
    )
    is_duplicate: bool = Field(
        default=False,
        nullable=False,
        description="Whether this transaction is a duplicate"
    )
    is_confirmed: bool = Field(
        default=False,
        nullable=False,
        description="Whether user has confirmed this transaction"
    )
    
    # Relationships
    statement: Statement = Relationship(back_populates="parsed_transactions")


class StatementFile(BaseModel, table=True):
    """Stores local file path references for statements"""
    
    __tablename__ = "statement_files"
    
    statement_id: UUID = Field(
        foreign_key="statements.id",
        nullable=False,
        unique=True,
        index=True,
        description="Reference to the statement"
    )
    local_file_path: str = Field(nullable=False, description="Local filesystem path to the file")
    file_hash: str = Field(nullable=False, index=True, description="SHA-256 hash of the file")
    
    # Relationships
    statement: Statement = Relationship(back_populates="statement_file")
