import pytest

from Helpers import Directory

class Tests_DirectoryExists:
    def test_DirectoryExists_None_Raises_ValueError(self):
        with pytest.raises(ValueError):
            Directory.DirectoryExists(None)

    def test_DirectoryExists_Int_Raises_ValueError(self):
        with pytest.raises(ValueError):
            Directory.DirectoryExists(9)

    def test_DirectoryExists_Returns_False_If_File(self):
        assert not Directory.DirectoryExists('./Helpers/File.py')

    def test_DirectoryExists_Returns_True_If_Directory_Exist(self):
        assert Directory.DirectoryExists('./Tests')

    def test_DirectoryExists_Returns_False_If_Directory_Doesnt_Exist(self):
        assert not Directory.DirectoryExists('./Temp')
