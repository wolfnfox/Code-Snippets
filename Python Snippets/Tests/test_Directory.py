import pytest

from helpers import directory

class Tests_directoryexists:
    def test_directoryexists_None_raises_ValueError(self):
        with pytest.raises(ValueError):
            directory.directoryexists(None)

    def test_directoryexists_int_raises_ValueError(self):
        with pytest.raises(ValueError):
            directory.directoryexists(9)

    def test_directoryexists_returns_False_if_file(self):
        assert not directory.directoryexists('./helpers/file.py')

    def test_directoryexists_returns_True_if_directory_exist(self):
        assert directory.directoryexists('./tests')

    def test_directoryexists_returns_False_if_directory_doesnt_exist(self):
        assert not directory.directoryexists('./temp')
