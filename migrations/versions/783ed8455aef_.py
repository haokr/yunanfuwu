"""empty message

Revision ID: 783ed8455aef
Revises: 3df81592d3ba
Create Date: 2020-06-05 10:56:17.265732

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '783ed8455aef'
down_revision = '3df81592d3ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ui_report_log', sa.Column('AphaseActivePower', sa.Float(), nullable=False, comment='A相有功功率'))
    op.add_column('ui_report_log', sa.Column('AphaseCurrent', sa.Float(), nullable=False, comment='A相电流'))
    op.add_column('ui_report_log', sa.Column('AphaseVoltage', sa.Float(), nullable=False, comment='A相电压'))
    op.add_column('ui_report_log', sa.Column('BphaseActivePower', sa.Float(), nullable=False, comment='B相有功功率'))
    op.add_column('ui_report_log', sa.Column('BphaseCurrent', sa.Float(), nullable=False, comment='B相电流'))
    op.add_column('ui_report_log', sa.Column('BphaseVoltage', sa.Float(), nullable=False, comment='B相电压'))
    op.add_column('ui_report_log', sa.Column('CphaseActivePpwer', sa.Float(), nullable=False, comment='C相有功功率'))
    op.add_column('ui_report_log', sa.Column('CphaseCurrent', sa.Float(), nullable=False, comment='C相电流'))
    op.add_column('ui_report_log', sa.Column('CphaseVoltage', sa.Float(), nullable=False, comment='c相电压'))
    op.add_column('ui_report_log', sa.Column('HighPositiveActiveTotalElectricEnergy', sa.Float(), nullable=False, comment='总电能'))
    op.add_column('ui_report_log', sa.Column('HighPositiveTotalReactivePower', sa.Float(), nullable=False, comment='总功率'))
    op.add_column('ui_report_log', sa.Column('TotalActivePowerHigh', sa.Float(), nullable=False, comment='总有功功率'))
    op.drop_column('ui_report_log', 'T2')
    op.drop_column('ui_report_log', 'T4')
    op.drop_column('ui_report_log', 'T1')
    op.drop_column('ui_report_log', 'L1')
    op.drop_column('ui_report_log', 'U1')
    op.drop_column('ui_report_log', 'U3')
    op.drop_column('ui_report_log', 'J1')
    op.drop_column('ui_report_log', 'I1')
    op.drop_column('ui_report_log', 'describe')
    op.drop_column('ui_report_log', 'I2')
    op.drop_column('ui_report_log', 'T3')
    op.drop_column('ui_report_log', 'I3')
    op.drop_column('ui_report_log', 'U2')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ui_report_log', sa.Column('U2', mysql.FLOAT(), nullable=False))
    op.add_column('ui_report_log', sa.Column('I3', mysql.FLOAT(), nullable=False))
    op.add_column('ui_report_log', sa.Column('T3', mysql.FLOAT(), nullable=False))
    op.add_column('ui_report_log', sa.Column('I2', mysql.FLOAT(), nullable=False))
    op.add_column('ui_report_log', sa.Column('describe', mysql.VARCHAR(length=30), nullable=True))
    op.add_column('ui_report_log', sa.Column('I1', mysql.FLOAT(), nullable=False))
    op.add_column('ui_report_log', sa.Column('J1', mysql.FLOAT(precision=8, scale=4), nullable=False))
    op.add_column('ui_report_log', sa.Column('U3', mysql.FLOAT(), nullable=False))
    op.add_column('ui_report_log', sa.Column('U1', mysql.FLOAT(), nullable=False))
    op.add_column('ui_report_log', sa.Column('L1', mysql.FLOAT(), nullable=False))
    op.add_column('ui_report_log', sa.Column('T1', mysql.FLOAT(), nullable=False))
    op.add_column('ui_report_log', sa.Column('T4', mysql.FLOAT(), nullable=False))
    op.add_column('ui_report_log', sa.Column('T2', mysql.FLOAT(), nullable=False))
    op.drop_column('ui_report_log', 'TotalActivePowerHigh')
    op.drop_column('ui_report_log', 'HighPositiveTotalReactivePower')
    op.drop_column('ui_report_log', 'HighPositiveActiveTotalElectricEnergy')
    op.drop_column('ui_report_log', 'CphaseVoltage')
    op.drop_column('ui_report_log', 'CphaseCurrent')
    op.drop_column('ui_report_log', 'CphaseActivePpwer')
    op.drop_column('ui_report_log', 'BphaseVoltage')
    op.drop_column('ui_report_log', 'BphaseCurrent')
    op.drop_column('ui_report_log', 'BphaseActivePower')
    op.drop_column('ui_report_log', 'AphaseVoltage')
    op.drop_column('ui_report_log', 'AphaseCurrent')
    op.drop_column('ui_report_log', 'AphaseActivePower')
    # ### end Alembic commands ###