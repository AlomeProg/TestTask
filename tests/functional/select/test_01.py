#coding:utf-8

"""
ID:          privilege-select-tc1
TITLE:       SELECT privilege not granted
DESCRIPTION: User without SELECT privilege tries to query a table and gets an error
FBTEST:      privileges.select.tc1
"""

import pytest
from firebird.qa import *

# fixture providing test database
db = db_factory()

# fixture providing test user without privileges
user = user_factory('db', name='tmp$user1', password='123')

# initial script to create a test table with some data
init_script = """
    recreate table test_table(id int, txt varchar(20));
    commit;
    insert into test_table values(1, 'alpha');
    insert into test_table values(2, 'beta');
    commit;
"""

# fixture to initialize database objects
act_init = isql_act('db', init_script)

# script executed by user without SELECT privilege
test_script = """
    connect '$(DSN)' user tmp$user1 password '123';
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
def test_select_without_privilege(act: Action, act_init: Action, user: User):
    # prepare table and data
    act_init.execute()
    # run test as user without SELECT privilege
    act.expected_stderr = expected_stderr
    act.execute()
    assert act.clean_stderr == act.clean_expected_stderr
