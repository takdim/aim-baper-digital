"""Add certificate_templates table

Revision ID: add_cert_templates
Revises: 2bb2e651de5a
Create Date: 2026-04-28

"""
from alembic import op
import sqlalchemy as sa


revision = 'add_cert_templates'
down_revision = '2bb2e651de5a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('certificate_templates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('certificate_number_format', sa.String(length=100), nullable=False),
    sa.Column('current_sequence', sa.Integer(), nullable=False, server_default='1'),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('head_name', sa.String(length=200), nullable=False),
    sa.Column('head_nip', sa.String(length=50), nullable=False),
    sa.Column('head_title', sa.String(length=100), nullable=True),
    sa.Column('institution_name', sa.String(length=200), nullable=True),
    sa.Column('institution_npp', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('course_id', name='uq_certificate_templates_course_id')
    )


def downgrade():
    op.drop_table('certificate_templates')
