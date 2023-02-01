"""init-tables

Revision ID: c1fb85880d50
Revises: 
Create Date: 2023-01-31 22:12:45.131878

"""
from alembic import op
from geoalchemy2 import Geometry
import sqlalchemy as sa
import logging

logging.basicConfig(filename='alembic.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# revision identifiers, used by Alembic.
revision = 'c1fb85880d50'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('create extension postgis;')
    op.create_table(
        'readings_airnow',
        sa.Column('station_name', sa.String(), nullable=False),
        sa.Column('reading_datetime', sa.DateTime(), nullable=False),
        sa.Column('request_datetime', sa.DateTime(), nullable=False),
        sa.Column('pm_10_conc', sa.Numeric(7, 3), nullable=True),
        sa.Column('pm_10_aqi', sa.Numeric(7, 3), nullable=True),
        sa.Column('pm_10_aqi_cat', sa.Numeric(2, 1), nullable=True),
        sa.Column('pm_25_conc', sa.Numeric(7, 3), nullable=True),
        sa.Column('pm_25_aqi', sa.Numeric(7, 3), nullable=True),
        sa.Column('pm_25_aqi_cat', sa.Numeric(2, 1), nullable=True),
        sa.PrimaryKeyConstraint('station_name', 'reading_datetime')
    )
    op.create_table(
        'readings_waqi',
        sa.Column('station_name', sa.String(), nullable=False),
        sa.Column('reading_datetime', sa.DateTime(), nullable=False),
        sa.Column('request_datetime', sa.DateTime(), nullable=False),
        sa.Column('latitude', sa.Numeric(10, 6), nullable=True),
        sa.Column('longitude', sa.Numeric(10, 6), nullable=True),
        sa.Column('pm_10', sa.Numeric(7, 3), nullable=True),
        sa.Column('pm_25', sa.Numeric(7, 3), nullable=True),
        sa.Column('co', sa.Numeric(7, 3), nullable=True),
        sa.Column('h', sa.Numeric(7, 3), nullable=True),
        sa.Column('no2', sa.Numeric(7, 3), nullable=True),
        sa.Column('o3', sa.Numeric(7, 3), nullable=True),
        sa.Column('p', sa.Numeric(7, 3), nullable=True),
        sa.Column('so2', sa.Numeric(7, 3), nullable=True),
        sa.Column('t', sa.Numeric(7, 3), nullable=True),
        sa.Column('w', sa.Numeric(7, 3), nullable=True),
        sa.Column('wg', sa.Numeric(7, 3), nullable=True),
        sa.PrimaryKeyConstraint('station_name', 'reading_datetime')
    )
    op.create_table(
        'stations_waqi',
        sa.Column('station_id', sa.Integer(), nullable=False),
        sa.Column('station_name', sa.String(), nullable=False),
        sa.Column('latitude', sa.Numeric(10, 6), nullable=False),
        sa.Column('longitude', sa.Numeric(10, 6), nullable=False),
        sa.Column('request_datetime', sa.DateTime(), nullable=True),
        sa.Column('data_datetime', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('station_id')
    )
    op.create_table(
        'stations_airnow',
        sa.Column('station_name', sa.String(), nullable=False),
        sa.Column('agency_name', sa.String(), nullable=False),
        sa.Column('latitude', sa.Numeric(10, 6), nullable=False),
        sa.Column('longitude', sa.Numeric(10, 6), nullable=False),
        sa.Column(
            'location_coord', Geometry(geometry_type='POINT'), nullable=False),
        sa.PrimaryKeyConstraint('station_name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stations_waqi')
    op.drop_table('readings_waqi')
    op.drop_table('readings_airnow')
    op.drop_table('stations_airnow')
    # ### end Alembic commands ###
