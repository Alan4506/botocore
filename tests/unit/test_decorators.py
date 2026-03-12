from unittest import mock

import pytest

from tests import requires_crt, skip_if_crt, skip_if_windows


class TestSkipIfWindows:
    def test_bare_skip_if_windows_fails_immediately(self):
        with pytest.raises(TypeError):

            @skip_if_windows
            def my_test():
                pass

    def test_skip_if_windows_skips_on_windows(self):
        with mock.patch('tests.platform') as mock_platform:
            mock_platform.system.return_value = 'Windows'

            @skip_if_windows('Not supported on Windows')
            def my_test():
                assert False

            assert getattr(my_test, '__unittest_skip__', False) is True

    def test_skip_if_windows_runs_on_non_windows(self):
        with mock.patch('tests.platform') as mock_platform:
            mock_platform.system.return_value = 'Linux'

            @skip_if_windows('Not supported on Windows')
            def my_test():
                pass

            assert getattr(my_test, '__unittest_skip__', False) is False


class TestRequiresCrt:
    def test_bare_requires_crt_fails_immediately(self):
        with pytest.raises(TypeError):

            @requires_crt
            def my_test():
                pass

    def test_requires_crt_skips_when_no_crt(self):
        with mock.patch('tests.HAS_CRT', False):

            @requires_crt()
            def my_test():
                assert False

            assert getattr(my_test, '__unittest_skip__', False) is True

    def test_requires_crt_runs_when_crt_available(self):
        with mock.patch('tests.HAS_CRT', True):

            @requires_crt()
            def my_test():
                pass

            assert getattr(my_test, '__unittest_skip__', False) is False


class TestSkipIfCrt:
    def test_bare_skip_if_crt_fails_immediately(self):
        with pytest.raises(TypeError):

            @skip_if_crt
            def my_test():
                pass

    def test_skip_if_crt_skips_when_crt_available(self):
        with mock.patch('tests.HAS_CRT', True):

            @skip_if_crt()
            def my_test():
                assert False

            assert getattr(my_test, '__unittest_skip__', False) is True

    def test_skip_if_crt_runs_when_no_crt(self):
        with mock.patch('tests.HAS_CRT', False):

            @skip_if_crt()
            def my_test():
                pass

            assert getattr(my_test, '__unittest_skip__', False) is False
