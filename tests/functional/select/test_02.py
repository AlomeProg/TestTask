#coding:utf-8

"""
ID:          privilege-select-tc2
TITLE:       SELECT privilege granted
DESCRIPTION: User with SELECT privilege is able to query a table successfully
FBTEST:      privileges.select.tc2
"""

import pytest
from firebird.qa import *

# fixture providing test database
db = db_factory()

# fixture providing test user
user = user_factory('db', name='tmp$user2', password='123')

# initial script to create a test table, insert data and grant SELECT privilege
init_script = """
    recreate table test_table(id int, txt varchar(20));
    commit;
    insert into test_table values(1, 'alpha');
    insert into test_table values(2, 'beta');
    commit;
    grant select on test_table to tmp$user2;
    commit;
"""

# fixture to initialize database objects
act_init = isql_act('db', init_script)

# script executed by user with SELECT privilege
test_script = """
    commit;
    connect '$(DSN)' user tmp$user2 password '123';
    set list on;
    select * from test_table;
"""

# fixture that provides Action object used in test function
act = isql_act('db', test_script)

# Expected stdout output from isql
expected_stdout = """
    ID                              1
    TXT                             alpha

    ID                              2
    TXT                             beta
"""

@pytest.mark.version('>=3.0')
def test_select_with_privilege(act: Action, act_init: Action, user: User):
    # prepare table and data, grant privilege
    act_init.execute()
    # run test as user with SELECT privilege
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
