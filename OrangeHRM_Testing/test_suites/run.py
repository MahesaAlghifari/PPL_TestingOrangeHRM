import pytest

test_dirs = [
    'login',
    'admin',
    'pim',
    'leave',
    'time',
    'recruitment',
    'myInfo',
    'performance',
    'dashboard',
    'directory',
    'maintenance',
    'claim',
    'buzz',
]

pytest.main(test_dirs + ["-v", "--html=report.html", "--self-contained-html"])
