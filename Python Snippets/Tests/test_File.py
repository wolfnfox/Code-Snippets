import pytest

from Helpers import File

class Tests_FileExists:
    def test_FileExists_None_Raises_ValueError(self):
        with pytest.raises(ValueError):
            File.FileExists(None)

    def test_FileExists_Bool_Raises_ValueError(self):
        with pytest.raises(ValueError):
            File.FileExists(True)

    def test_FileExists_Int_Raises_ValueError(self):
        with pytest.raises(ValueError):
            File.FileExists(9)
    
    def test_FileExists_Float_Raises_ValueError(self):
        with pytest.raises(ValueError):
            File.FileExists(9.9)

    def test_FileExists_Returns_False_If_Directory(self):
        assert not File.FileExists('./Tests')

    def test_FileExists_Returns_True_If_File_Exist(self):
        assert File.FileExists('./Helpers/File.py')

    def test_FileExists_Returns_False_If_File_Doesnt_Exist(self):
        assert not File.FileExists('./Helpers/Files.py')

class Tests_FileSize:
    def test_FileSize_None_Raises_ValueError(self):
        with pytest.raises(ValueError):
            File.FileSize(None)

    def test_FileExists_Bool_Raises_ValueError(self):
        with pytest.raises(ValueError):
            File.FileSize(True)

    def test_FileExists_Int_Raises_ValueError(self):
        with pytest.raises(ValueError):
            File.FileSize(9)
    
    def test_FileExists_Float_Raises_ValueError(self):
        with pytest.raises(ValueError):
            File.FileSize(9.9)

    def test_FileSize_Raises_FileNotFound_If_File_Doesnt_Exist(self):
        with pytest.raises(FileNotFoundError):
            File.FileSize('./Tests/Data/Fake.docx')
    
    @pytest.mark.parametrize("filename,units,expected", [('./Tests/Data/Word.docx',None, 296), ('./Tests/Data/Word.docx','B', 302577), ('./Tests/Data/Word.docx','KB', 296), ('./Tests/Data/Word.docx','MB', 0.28856)])
    def test_FileSize_Returns_FileSize_Number(self,filename,units,expected):
        assert File.FileSize(filename,units) == expected
