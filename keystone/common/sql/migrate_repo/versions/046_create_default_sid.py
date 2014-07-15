# Copyright 2012 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json

import sqlalchemy as sql
from sqlalchemy import orm

from keystone import config


CONF = config.CONF


def upgrade(migrate_engine):
    """Creates the default sid."""
    meta = sql.MetaData()
    meta.bind = migrate_engine

    sid_table = sql.Table('sid', meta, autoload=True)

    sid = {
        'id': CONF.identity.default_sid_id,
        'name': 'Default',
        'enabled': True,
        'extra': json.dumps({
            'description': 'It is default sid for all sips.'})}

    session = orm.sessionmaker(bind=migrate_engine)()
    insert = sid_table.insert()
    insert.execute(sid)
    session.commit()


def downgrade(migrate_engine):
    """Delete the default sid."""
    meta = sql.MetaData()
    meta.bind = migrate_engine

    sql.Table('sid', meta, autoload=True)
    session = orm.sessionmaker(bind=migrate_engine)()
    session.execute(
        'DELETE FROM sid WHERE id=:id',
        {'id': CONF.identity.default_sid_id})
    session.commit()


