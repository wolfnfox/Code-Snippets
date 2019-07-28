import pytest

from helpers import file

class Tests_fileexists:
    def test_fileexists_None_raises_ValueError(self):
        with pytest.raises(ValueError):
            file.fileexists(None)

    def fileexists_bool_raises_ValueError(self):
        with pytest.raises(ValueError):
            file.fileexists(True)

    def test_fileexists_int_raises_ValueError(self):
        with pytest.raises(ValueError):
            file.fileexists(9)
    
    def test_fileexists_float_raises_ValueError(self):
        with pytest.raises(ValueError):
            file.fileexists(9.9)

    def test_fileexists_returns_False_if_directory(self):
        assert not file.fileexists('./tests')

    def test_fileexists_returns_True_if_fileexists(self):
        assert file.fileexists('./helpers/file.py')

    def test_fileexists_returns_False_if_file_doesnt_exist(self):
        assert not file.fileexists('./helpers/files.py')

class Tests_filesize:
    def test_filesize_None_raises_ValueError(self):
        with pytest.raises(ValueError):
            file.filesize(None)

    def test_filesize_bool_raises_ValueError(self):
        with pytest.raises(ValueError):
            file.filesize(True)

    def test_filesize_int_raises_ValueError(self):
        with pytest.raises(ValueError):
            file.filesize(9)
    
    def test_filesize_float_raises_ValueError(self):
        with pytest.raises(ValueError):
            file.filesize(9.9)

    def test_filesize_raises_FileNotFound_if_file_doesnt_exist(self):
        with pytest.raises(FileNotFoundError):
            file.filesize('./tests/data/fake.docx')
    
    @pytest.mark.parametrize("filename,units,expected", [('./tests/data/word.docx',None, 296), ('./tests/data/word.docx','B', 302577), ('./tests/data/word.docx','KB', 296), ('./tests/data/word.docx','MB', 0.289)])
    def test_filesize_returns_filesize(self,filename,units,expected):
        assert file.filesize(filename,units) == expected
