import os
import re

DATA_VERSION = 1
FILE_PREFIX = "v{}_".format(DATA_VERSION)
VERSION_FILE_NAME = "VERSION"

def assert_version(data_directory):
    version_file = os.path.join(data_directory, VERSION_FILE_NAME)

    try:
        assert os.path.exists(version_file), "more"
        with open(version_file, 'r') as f:
            try:
                txt = int(f.read())
            except Exception as e:
                raise AssertionError("less")
            current_version = txt

        assert DATA_VERSION <= txt, "more"
        assert DATA_VERSION >= txt, "less"
    except AssertionError as e:
        _raise_error(e,data_directory)


def assert_prefix(tail):
    """Asserts that a file name satifies a certain prefix.
    
    Args:
        file_name (str): The file name to test.
    """
    try:
        assert os.path.exists(tail), "File {} does not exist.".format(tail)

        m = re.search('v([0-9]+?)_', tail)
        assert bool(m), "more"
        ver = int(m.group(1))

        assert DATA_VERSION <= ver, "more"
        assert DATA_VERSION >= ver, "less"


    except AssertionError as e:
        _raise_error(e)

def _raise_error(exception, directory=None):
    comparison = str(exception)
    if comparison == "more":
        if directory:
            dir_str = "direction={}".format(directory)
        else:
            dir_str = ""
        e =  RuntimeError(
            "YOUR DATASET IS OUT OF DATE! The latest is on version v{} but yours is lower!\n\n"
            "\tRe-download the data using `minerl.data.download({})`".format(
                DATA_VERSION, dir_str))
        e.comparison = comparison
        raise e
    elif comparison == "less":
        e = RuntimeError("YOUR MINERL PACKAGE IS OUT OF DATE! \n\n\tPlease upgrade with `pip3 install --upgrade minerl`")
        e.comparison = comparison
        raise e
    else:
        raise exception

