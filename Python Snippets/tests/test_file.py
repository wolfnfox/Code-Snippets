import os, pytest, shutil

from helpers import file

class Tests_copy:
    @pytest.mark.parametrize('filename', [(None,True,9,9.9)])
    def test_copy_nonstr_raises_ValueError(self,filename):
        with pytest.raises(ValueError):
            file.copy(filename)
    
    def test_copy_raises_FileNotFoundError(self):
        with pytest.raises(FileNotFoundError):
            file.copy('./tests/data/fake.docx')

    @pytest.mark.parametrize('filename,newfilename,expected', [('./tests/data/word.docx',None,'./tests/data/word(1).docx'),('./tests/data/word.docx','./tests/data/word(new).docx','./tests/data/word(new).docx')])
    def test_copy_filename_returns_newfilename(self,filename,newfilename,expected):
        newfilename = file.copy(filename,newfilename)
        os.remove(newfilename)
        assert newfilename == expected

    def test_copy_filename_overwrites_filename(self):
        shutil.copy2('./tests/data/word.docx','./tests/data/word-copy.docx')
        newfilename = file.copy('./tests/data/word-copy.docx',overwrite=True)
        os.remove(newfilename)
        assert newfilename == './tests/data/word-copy.docx'

class Tests_delete:
    @pytest.mark.parametrize('filename', [(None,True,9,9.9)])
    def test_delete_nonstr_raises_ValueError(self,filename):
        with pytest.raises(ValueError):
            file.delete(filename)

    @pytest.mark.parametrize('filename', [('./tests/data/fake.docx','./tests/data/temp')])
    def test_delete_raises_FileNotFoundError(self,filename):
        with pytest.raises(FileNotFoundError):
            file.delete('./tests/data/fake.docx')

    def test_delete_filename(self):
        filename = './tests/data/temp.txt'
        with open(filename,'wt') as fopen:
            fopen.write('test')
        assert file.delete(filename)

class Tests_fileexists:
    @pytest.mark.parametrize('filename', [(None,True,9,9.9)])
    def test_fileexists_nonstr_raises_ValueError(self,filename):
        with pytest.raises(ValueError):
            file.fileexists(None)

    def test_fileexists_returns_False_if_directory(self):
        assert not file.fileexists('./tests')

    def test_fileexists_returns_True_if_fileexists(self):
        assert file.fileexists('./helpers/file.py')

    def test_fileexists_returns_False_if_file_doesnt_exist(self):
        assert not file.fileexists('./helpers/files.py')

class Tests_filesize:
    @pytest.mark.parametrize('filename', [(None,True,9,9.9)])
    def test_filesize_nonstr_raises_ValueError(self,filename):
        with pytest.raises(ValueError):
            file.filesize(filename)

    def test_filesize_raises_FileNotFound_if_file_doesnt_exist(self):
        with pytest.raises(FileNotFoundError):
            file.filesize('./tests/data/fake.docx')
    
    @pytest.mark.parametrize('filename,units,expected', [('./tests/data/word.docx',None, 296), ('./tests/data/word.docx','B', 302577), ('./tests/data/word.docx','KB', 296), ('./tests/data/word.docx','MB', 0.289)])
    def test_filesize_returns_filesize(self,filename,units,expected):
        assert file.filesize(filename,units) == expected

class Tests_getextension:
    @pytest.mark.parametrize('filename', [(None,True,9,9.9)])
    def test_getextension_nonstr_raises_ValueError(self,filename):
        with pytest.raises(ValueError):
            file.getextension(filename)

    @pytest.mark.parametrize('filename,expected',[('test.pdf','.pdf'),('testfile',''),('C:\test','')])
    def test_getextension_returns_extension(self,filename,expected):
        assert file.getextension(filename) == expected

class Tests_incrementfilename:
    @pytest.mark.parametrize('filename', [(None,True,9,9.9)])
    def test_getextension_nonstr_raises_ValueError(self,filename):
        with pytest.raises(ValueError):
            file._incrementfilename(filename)

    @pytest.mark.parametrize('filename,expected', [('./tests/data/fake.docx','./tests/data/fake.docx'),('./tests/data/word.docx','./tests/data/word(1).docx')])
    def test_incrementfilename_returns_newfilename(self,filename,expected):
        assert file._incrementfilename(filename) == expected
