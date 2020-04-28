import pytest
import sys
import os
import shutil
import pathlib

@pytest.fixture
def setup(monkeypatch):
    expected = [
        '00_input.txt',
        '00_output.txt',
        '01_input.txt',
        '01_output.txt']
    monkeypatch.setattr('os.listdir', lambda _: expected)
    yield

@pytest.fixture(scope='function')
def setup_test_files(tmpdir):
    tmpfile_00in = tmpdir.join('00_input.txt')
    tmpfile_00out = tmpdir.join('00_output.txt')
    tmpfile_01in = tmpdir.join('01_input.txt')
    tmpfile_01out = tmpdir.join('01_output.txt')
    with tmpfile_00in.open('w') as f: f.write('1 2 3')
    with tmpfile_00out.open('w') as f: f.write('1 2 3\n')
    with tmpfile_01in.open('w') as f: f.write('4 5 6')
    with tmpfile_01out.open('w') as f: f.write('4 5 6\n')
    mock_test_files = list(map(str,[
        tmpfile_00in,
        tmpfile_00out,
        tmpfile_01in,
        tmpfile_01out]))

    yield mock_test_files

    # clean up tmpdir
    tmpfile_00in.remove()
    tmpfile_00out.remove()
    tmpfile_01in.remove()
    tmpfile_01out.remove()
    """
    本来は自動で過去のtmpdirが削除されるようだが、
    macOS環境下ではtmpdir下にディレクトリのエイリアスが作成され、
    tmpdirのclean up時にエイリアスが削除されず、
    ディレクトリが空でないとのエラーが発生し結果tmpdirが残ったままになる。
    そのため、明示的に削除を行っている。
    """
    tmp_test_dir = str(pathlib.Path(tmpdir).parent) + '/'
    shutil.rmtree(tmp_test_dir)

@pytest.fixture
def setup_run_target():
    with open('sample.py', 'w') as f:
        f.write("""
import sys
print(sys.stdin.readline())
""")
    yield 'sample.py'
    os.remove('sample.py')
