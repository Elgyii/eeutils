import os


def rm_file(file: str, ext: int = 0):
    """
    Removes a given file
    :param file: file to remove
    :return: system exit
    """
    if os.name == 'nt':
        ext = os.system(f'del /f {file} >nul')
    if os.name == 'posix':
        ext = os.system(f'rm -f {file} 2> /dev/null')
    return ext
