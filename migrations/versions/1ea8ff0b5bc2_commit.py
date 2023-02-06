"""commit

Revision ID: 1ea8ff0b5bc2
Revises: d464d069c4dd
Create Date: 2023-02-05 18:55:07.243900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ea8ff0b5bc2'
down_revision = 'd464d069c4dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hero', schema=None) as batch_op:
        batch_op.add_column(sa.Column('img_head', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hero', schema=None) as batch_op:
        batch_op.drop_column('img_head')

    # ### end Alembic commands ###