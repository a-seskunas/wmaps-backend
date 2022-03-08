import dir_fetch
import pytest

def test_competion():
    file_name = 'stuff000.grb2'
    if dir_fetch.main(file_name, 10, 60, 150, 245, 'SD_N', 32.7, 242.85, 9, 160, 310, 25, 16, False):
        pytest.fail("Method dir_fetch failed to complete")

