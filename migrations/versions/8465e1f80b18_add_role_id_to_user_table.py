"""Add role_id to user table

Revision ID: 8465e1f80b18
Revises: 93391aa2a459
Create Date: 2024-07-09 23:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '8465e1f80b18'
down_revision = '93391aa2a459'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_user_role_id', 'role', ['role_id'], ['id'])

def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('fk_user_role_id', type_='foreignkey')
        batch_op.drop_column('role_id')