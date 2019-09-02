import os, pytest, shutil

from helpers import file

class Tests_append_all_text:
    @pytest.mark.parametrize('text,filename,encoding',
    [(None,None,None),
     ('test',None,None),
     ('test','test.txt',None)])
    def test_non_str_raises_ValueError(self,text,filename,encoding):
        with pytest.raises(ValueError):
            file.append_all_text(text,filename,encoding)
    
    def test_raises_FileNotFoundError(self):
        with pytest.raises(FileNotFoundError):
            file.append_all_text('test','fake.txt')

    def test_writes_text_to_file(self):
        with open('./tests/data/test.txt','wt') as fopen:
            fopen.write('test')
        file.append_all_text('test','./tests/data/test.txt')
        with open('./tests/data/test.txt','rt') as fopen:
            data = fopen.read()
        os.remove('./tests/data/test.txt')
        assert data == 'testtest'

class Tests_copy:
    @pytest.mark.parametrize('filename', [(None,True,9,9.9)])
    def test_non_str_raises_ValueError(self,filename):
        with pytest.raises(ValueError):
            file.copy(filename)
    
    def test_raises_FileNotFoundError(self):
        with pytest.raises(FileNotFoundError):
            file.copy('./tests/data/fake.docx')

    @pytest.mark.parametrize('filename,newfilename,expected', [('./tests/data/word.docx',None,'./tests/data/word(1).docx'),('./tests/data/word.docx','./tests/data/word(new).docx','./tests/data/word(new).docx')])
    def test_copying_filename_returns_newfilename(self,filename,newfilename,expected):
        newfilename = file.copy(filename,newfilename)
        os.remove(newfilename)
        assert newfilename == expected

    def test_copying_filename_overwrites_filename(self):
        shutil.copy2('./tests/data/word.docx','./tests/data/word-copy.docx')
        newfilename = file.copy('./tests/data/word-copy.docx',overwrite=True)
        os.remove(newfilename)
        assert newfilename == './tests/data/word-copy.docx'

class Tests_delete:
    @pytest.mark.parametrize('filename', [(None,True,9,9.9)])
    def test_non_str_raises_ValueError(self,filename):
        with pytest.raises(ValueError):
            file.delete(filename)

    @pytest.mark.parametrize('filename', [('./tests/data/fake.docx','./tests/data/temp')])
    def test_raises_FileNotFoundError(self,filename):
        with pytest.raises(FileNotFoundError):
            file.delete('./tests/data/fake.docx')

    def test_deletes_filename(self):
        filename = './tests/data/temp.txt'
        with open(filename,'wt') as fopen:
            fopen.write('test')
        assert file.delete(filename)

class Tests_fileexists:
    @pytest.mark.parametrize('filename', [(None,True,9,9.9)])
    def test_non_str_raises_ValueError(self,filename):
        with pytest.raises(ValueError):
            file.fileexists(None)

    def test_returns_False_if_directory(self):
        assert not file.fileexists('./tests')

    def test_returns_True_if_fileexists(self):
        assert file.fileexists('./helpers/file.py')

    def test_returns_False_if_file_doesnt_exist(self):
        assert not file.fileexists('./helpers/files.py')

class Tests_filesize:
    @pytest.mark.parametrize('filename', [(None,True,9,9.9)])
    def test_non_str_raises_ValueError(self,filename):
        with pytest.raises(ValueError):
            file.filesize(filename)

    def test_raises_FileNotFound_if_file_doesnt_exist(self):
        with pytest.raises(FileNotFoundError):
            file.filesize('./tests/data/fake.docx')
    
    @pytest.mark.parametrize('filename,units,expected', [('./tests/data/word.docx',None, 296), ('./tests/data/word.docx','B', 302577), ('./tests/data/word.docx','KB', 296), ('./tests/data/word.docx','MB', 0.289)])
    def test_returns_filesize(self,filename,units,expected):
        assert file.filesize(filename,units) == expected

class Tests_get_extension:
    @pytest.mark.parametrize('filename', [(None,True,9,9.9)])
    def test_non_str_raises_ValueError(self,filename):
        with pytest.raises(ValueError):
            file.get_extension(filename)

    @pytest.mark.parametrize('filename,expected',[('test.pdf','.pdf'),('testfile',''),('C:\test','')])
    def test_returns_extension(self,filename,expected):
        assert file.get_extension(filename) == expected

class Tests_read_all_bytes:
    @pytest.mark.parametrize('filename',[None,True,6,3.7])
    def test_raises_ValueError(self,filename):
        with pytest.raises(ValueError):
            file.read_all_bytes(filename)
    
    def test_raises_FileNotFoundError(self):
        with pytest.raises(FileNotFoundError):
            file.read_all_bytes('fake.txt')

    def test_reads_bytes(self):
        with open('./tests/data/test.txt','wb') as fopen:
            fopen.write(b'test')
        file.read_all_bytes('./tests/data/test.txt')
        with open('./tests/data/test.txt','rb') as fopen:
            data = fopen.read()
        os.remove('./tests/data/test.txt')
        assert data == b'test'

class Tests_read_all_text:
    @pytest.mark.parametrize('filename,encoding',
    [(None,'utf-8'),(True,'utf-8'),(6,'utf-8'),(3.7,'utf-8'),('test.txt',None)])
    def test_non_str_raises_ValueError(self,filename,encoding):
        with pytest.raises(ValueError):
            file.read_all_text(filename,encoding)
    
    def test_raises_FileNotFoundError(self):
        with pytest.raises(FileNotFoundError):
            file.read_all_text('fake.txt')

    def test_reads_text(self):
        with open('./tests/data/test.txt','wt') as fopen:
            fopen.write('test')
        data = file.read_all_text('./tests/data/test.txt')
        os.remove('./tests/data/test.txt')
        assert data == 'test'

class Tests_increment_filename:
    @pytest.mark.parametrize('filename', [(None,True,9,9.9)])
    def test_non_str_raises_ValueError(self,filename):
        with pytest.raises(ValueError):
            file._increment_filename(filename)

    @pytest.mark.parametrize('filename,expected', [('./tests/data/fake.docx','./tests/data/fake.docx'),('./tests/data/word.docx','./tests/data/word(1).docx')])
    def test_returns_newfilename(self,filename,expected):
        assert file._increment_filename(filename) == expected
