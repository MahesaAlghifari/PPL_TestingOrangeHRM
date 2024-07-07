import pytest

test_dirs = [
    'login',
    'admin',
    'buzz',
    'dashboard',
    'directory',
    'leave',
    'myinfo',
    'performance',
    'pim',
    'recruitment',
    'time'
]

pytest.main(test_dirs + ["-v", "--html=report.html", "--self-contained-html"])
