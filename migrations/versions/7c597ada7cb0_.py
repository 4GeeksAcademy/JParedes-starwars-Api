"""empty message

Revision ID: 7c597ada7cb0
Revises: ea771c2c1347
Create Date: 2023-08-23 19:05:09.036087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c597ada7cb0'
down_revision = 'ea771c2c1347'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.alter_column('birth_year',
               existing_type=sa.DATE(),
               type_=sa.String(length=250),
               existing_nullable=True)
        batch_op.alter_column('species',
               existing_type=sa.VARCHAR(length=250),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.alter_column('species',
               existing_type=sa.VARCHAR(length=250),
               nullable=False)
        batch_op.alter_column('birth_year',
               existing_type=sa.String(length=250),
               type_=sa.DATE(),
               existing_nullable=True)

    # ### end Alembic commands ###
