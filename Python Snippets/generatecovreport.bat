call C:\ProgramData\Anaconda3\Scripts\activate.bat
call pytest --cov-report xml:cov.xml --cov=helpers
call conda deactivate