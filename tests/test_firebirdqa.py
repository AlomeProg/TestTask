#coding:utf-8

"""
ID:          issue-319
ISSUE:       319
JIRA:        CORE-1
TITLE:       Server shutdown
DESCRIPTION: Server shuts down when user password is attempted to be modified to a empty string
FBTEST:      bugs.core_0001
"""

import pytest
from firebird.qa import *

# fixture providing test database
db = db_factory()

# fixture providing temporary user
user = user_factory('db', name='tmp$c0001', password='123')

# isql script executed to test Firebird
test_script = """
    alter user tmp$c0001 password '';
    commit;
"""

# fixture that provides Action object used in test function
act = isql_act('db', test_script)

# Expected stderr output from isql
expected_stderr = """
    Statement failed, SQLSTATE = 42000
    unsuccessful metadata update
    -ALTER USER TMP$C0001 failed
    -Password should not be empty string
"""

# Test function, marked to run on Firebird v3.0 or newer
@pytest.mark.version('>=3.0')
def test_1(act: Action, user: User):
    act.expected_stderr = expected_stderr
    act.execute()
    # This evaluates test outcome
    assert act.clean_stderr == act.clean_expected_stderr