#coding:utf-8

"""
ID:          privilege-select-tc3
TITLE:       SELECT privilege revoked
DESCRIPTION: User loses SELECT privilege after REVOKE and gets an error on query
FBTEST:      privileges.select.tc3
"""

import pytest
from firebird.qa import *

# fixture providing test database
db = db_factory()

# fixture providing test user
user = user_factory('db', name='tmp$user3', password='123')

# initial script: create table, insert data, grant SELECT, then revoke
init_script = """
    recreate table test_table(id int, txt varchar(20));
    commit;
    insert into test_table values(1, 'alpha');
    insert into test_table values(2, 'beta');
    commit;
    grant select on test_table to tmp$user3;
    commit;
    revoke select on test_table from tmp$user3;
    commit;
"""

# fixture to initialize database objects
act_init = isql_act('db', init_script)

# script executed by user after privilege was revoked
test_script = """
    connect '$(DSN)' user tmp$user3 password '123';
    set list on;
    select * from test_table;
"""

# fixture that provides Action object used in test function
act = isql_act('db', test_script, substitutions=[('^((?!SQLSTATE).)*$', '')])

# Expected stderr output from isql
expected_stderr = """
    Statement failed, SQLSTATE = 28000
    no permission for SELECT access to TABLE TEST_TABLE
"""

@pytest.mark.version('>=3.0')
def test_select_revoked(act: Action, act_init: Action, user: User):
    # prepare table, grant and then revoke privilege
    act_init.execute()
    # run test as user with revoked SELECT privilege
    act.expected_stderr = expected_stderr
    act.execute()
    assert act.clean_stderr == act.clean_expected_stderr
