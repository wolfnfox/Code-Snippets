call C:\ProgramData\Anaconda3\Scripts\activate.bat
call pytest --cov-report xml:cov.xml --cov=.
call conda deactivate