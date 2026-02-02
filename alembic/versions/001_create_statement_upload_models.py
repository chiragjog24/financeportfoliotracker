"""Create statement upload data models

Revision ID: 001_create_statement_upload_models
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_create_statement_upload_models'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum types
    op.execute("CREATE TYPE uploadsessionstatus AS ENUM ('pending', 'processing', 'completed', 'failed', 'expired')")
    op.execute("CREATE TYPE statementtype AS ENUM ('cams', 'kfintech', 'zerodha', 'pms', 'aif', 'manual')")
    op.execute("CREATE TYPE transactiontype AS ENUM ('purchase', 'sale', 'dividend', 'interest', 'redemption', 'switch', 'sip', 'stp', 'swp', 'bonus', 'split', 'other')")
    
    # Create upload_sessions table
    op.create_table(
        'upload_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('status', postgresql.ENUM('pending', 'processing', 'completed', 'failed', 'expired', name='uploadsessionstatus'), nullable=False),
        sa.Column('statement_type', postgresql.ENUM('cams', 'kfintech', 'zerodha', 'pms', 'aif', 'manual', name='statementtype'), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_upload_sessions_id'), 'upload_sessions', ['id'], unique=False)
    op.create_index(op.f('ix_upload_sessions_user_id'), 'upload_sessions', ['user_id'], unique=False)
    
    # Create statements table
    op.create_table(
        'statements',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('upload_session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('file_name', sa.String(), nullable=False),
        sa.Column('file_size_bytes', sa.Integer(), nullable=False),
        sa.Column('statement_type', postgresql.ENUM('cams', 'kfintech', 'zerodha', 'pms', 'aif', 'manual', name='statementtype'), nullable=False),
        sa.Column('statement_date', sa.DateTime(), nullable=True),
        sa.Column('institution_name', sa.String(), nullable=True),
        sa.Column('folio_number', sa.String(), nullable=True),
        sa.Column('parsing_confidence', sa.Numeric(), nullable=True),
        sa.Column('confirmed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['upload_session_id'], ['upload_sessions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_statements_id'), 'statements', ['id'], unique=False)
    op.create_index(op.f('ix_statements_user_id'), 'statements', ['user_id'], unique=False)
    op.create_index(op.f('ix_statements_upload_session_id'), 'statements', ['upload_session_id'], unique=False)
    op.create_index(op.f('ix_statements_folio_number'), 'statements', ['folio_number'], unique=False)
    
    # Create parsed_transactions table
    op.create_table(
        'parsed_transactions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('statement_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('transaction_type', postgresql.ENUM('purchase', 'sale', 'dividend', 'interest', 'redemption', 'switch', 'sip', 'stp', 'swp', 'bonus', 'split', 'other', name='transactiontype'), nullable=False),
        sa.Column('transaction_date', sa.DateTime(), nullable=False),
        sa.Column('security_name', sa.String(), nullable=True),
        sa.Column('security_symbol', sa.String(), nullable=True),
        sa.Column('quantity', sa.Numeric(), nullable=True),
        sa.Column('price_per_unit', sa.Numeric(), nullable=True),
        sa.Column('nav', sa.Numeric(), nullable=True),
        sa.Column('amount', sa.Numeric(), nullable=True),
        sa.Column('units', sa.Numeric(), nullable=True),
        sa.Column('brokerage_charges', sa.Numeric(), nullable=True),
        sa.Column('confidence_score', sa.Numeric(), nullable=True),
        sa.Column('is_duplicate', sa.Boolean(), nullable=False),
        sa.Column('is_confirmed', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['statement_id'], ['statements.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_parsed_transactions_id'), 'parsed_transactions', ['id'], unique=False)
    op.create_index(op.f('ix_parsed_transactions_user_id'), 'parsed_transactions', ['user_id'], unique=False)
    op.create_index(op.f('ix_parsed_transactions_statement_id'), 'parsed_transactions', ['statement_id'], unique=False)
    op.create_index(op.f('ix_parsed_transactions_transaction_date'), 'parsed_transactions', ['transaction_date'], unique=False)
    op.create_index(op.f('ix_parsed_transactions_security_symbol'), 'parsed_transactions', ['security_symbol'], unique=False)
    
    # Create statement_files table
    op.create_table(
        'statement_files',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('statement_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('local_file_path', sa.String(), nullable=False),
        sa.Column('file_hash', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['statement_id'], ['statements.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('statement_id')
    )
    op.create_index(op.f('ix_statement_files_id'), 'statement_files', ['id'], unique=False)
    op.create_index(op.f('ix_statement_files_statement_id'), 'statement_files', ['statement_id'], unique=True)
    op.create_index(op.f('ix_statement_files_file_hash'), 'statement_files', ['file_hash'], unique=False)


def downgrade() -> None:
    # Drop tables
    op.drop_index(op.f('ix_statement_files_file_hash'), table_name='statement_files')
    op.drop_index(op.f('ix_statement_files_statement_id'), table_name='statement_files')
    op.drop_index(op.f('ix_statement_files_id'), table_name='statement_files')
    op.drop_table('statement_files')
    
    op.drop_index(op.f('ix_parsed_transactions_security_symbol'), table_name='parsed_transactions')
    op.drop_index(op.f('ix_parsed_transactions_transaction_date'), table_name='parsed_transactions')
    op.drop_index(op.f('ix_parsed_transactions_statement_id'), table_name='parsed_transactions')
    op.drop_index(op.f('ix_parsed_transactions_user_id'), table_name='parsed_transactions')
    op.drop_index(op.f('ix_parsed_transactions_id'), table_name='parsed_transactions')
    op.drop_table('parsed_transactions')
    
    op.drop_index(op.f('ix_statements_folio_number'), table_name='statements')
    op.drop_index(op.f('ix_statements_upload_session_id'), table_name='statements')
    op.drop_index(op.f('ix_statements_user_id'), table_name='statements')
    op.drop_index(op.f('ix_statements_id'), table_name='statements')
    op.drop_table('statements')
    
    op.drop_index(op.f('ix_upload_sessions_user_id'), table_name='upload_sessions')
    op.drop_index(op.f('ix_upload_sessions_id'), table_name='upload_sessions')
    op.drop_table('upload_sessions')
    
    # Drop enum types
    op.execute('DROP TYPE IF EXISTS transactiontype')
    op.execute('DROP TYPE IF EXISTS statementtype')
    op.execute('DROP TYPE IF EXISTS uploadsessionstatus')
