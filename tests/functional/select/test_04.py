#coding:utf-8

"""
ID:          privilege-select-tc4
TITLE:       Revoke SELECT privilege twice
DESCRIPTION: Test behavior when REVOKE SELECT is executed twice on the same user/table.
FBTEST:      privileges.select.tc4
"""

import pytest
from firebird.qa import *

# fixture providing test database
db = db_factory()

# fixture providing test user
user = user_factory('db', name='tmp$user1', password='123')

# initial script to create a test table, insert data and grant SELECT privilege
init_script = """
    recreate table test_table(id int, txt varchar(20));
    commit;
    insert into test_table values(1, 'alpha');
    insert into test_table values(2, 'beta');
    commit;
    grant select on test_table to tmp$user1;
    commit;
"""

# fixture to initialize database objects
act_init = isql_act('db', init_script)

# script executed by user with SELECT privilege
test_script = """
    revoke select on test_table from tmp$user1;
    revoke select on test_table from tmp$user1;
"""

# fixture that provides Action object used in test function
act = isql_act('db', test_script)

# Expected stdout output from isql
expected_stderr = """
Warning: SELECT on TEST_TABLE is not granted to TMP$USER1.
"""

@pytest.mark.version('>=3.0')
def test_double_revoke(act: Action, act_init: Action, user: User):
    # prepare table and data, grant privilege
    act_init.execute()
    # run test 
    act.expected_stderr = expected_stderr
    act.execute()
    assert act.clean_stderr == act.clean_expected_stderr
