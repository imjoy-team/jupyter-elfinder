"""Test elfinder."""
from jupyter_elfinder.api_const import (
    API_CMD,
    API_INIT,
    API_TARGET,
    API_TARGETS,
    API_TREE,
    API_TYPE,
    R_ADDED,
    R_API,
    R_CWD,
    R_DIM,
    R_ERROR,
    R_FILES,
    R_NETDRIVERS,
    R_OPTIONS,
    R_UPLMAXFILE,
    R_UPLMAXSIZE,
)
from jupyter_elfinder.elfinder import make_hash
from jupyter_elfinder.views import connector


def test_open(p_request, settings):
    """Test the open command."""
    p_request.params[API_CMD] = "open"
    p_request.params[API_INIT] = True
    p_request.params[API_TREE] = True
    p_request.params[API_TARGET] = None
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert R_ERROR not in body
    assert body[R_API] >= 2.1
    assert R_CWD in body
    assert R_NETDRIVERS in body
    assert R_FILES in body
    # Optional
    assert R_UPLMAXFILE in body
    assert R_UPLMAXSIZE in body
    assert R_OPTIONS in body


def test_archive(p_request, settings, txt_file):
    """Test the archive command."""
    p_request.params[API_CMD] = "archive"
    p_request.params[API_TYPE] = "application/x-tar"
    p_request.params[API_TARGET] = make_hash(str(txt_file.parent))
    p_request.params[API_TARGETS] = make_hash(str(txt_file))
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert R_ERROR not in body
    assert "added" in body


def test_archive_errors(p_request, settings, txt_file):
    """Test the archive command with errors."""
    # Invalid parameters
    p_request.params[API_CMD] = "archive"
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert R_ERROR in body

    p_request.params.clear()
    p_request.params[API_CMD] = "archive"
    p_request.params[API_TYPE] = "application/x-tar"
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert R_ERROR in body

    p_request.params.clear()
    p_request.params[API_CMD] = "archive"
    p_request.params[API_TYPE] = "application/x-tar"
    p_request.params[API_TARGET] = make_hash(str(txt_file.parent))
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert R_ERROR in body

    p_request.params.clear()
    p_request.params[API_CMD] = "archive"
    p_request.params[API_TYPE] = "application/x-tar"
    p_request.params[API_TARGETS] = make_hash(str(txt_file))
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert R_ERROR in body

    p_request.params.clear()
    p_request.params[API_CMD] = "archive"
    p_request.params[API_TARGET] = make_hash(str(txt_file.parent))
    p_request.params[API_TARGETS] = make_hash(str(txt_file))
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert R_ERROR in body

    # Incorrect archive type
    p_request.params.clear()
    p_request.params[API_CMD] = "archive"
    p_request.params[API_TYPE] = "missing"
    p_request.params[API_TARGET] = make_hash(str(txt_file.parent))
    p_request.params[API_TARGETS] = make_hash(str(txt_file))
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert R_ERROR in body

    # Bad target directory
    p_request.params.clear()
    p_request.params[API_CMD] = "archive"
    p_request.params[API_TYPE] = "application/x-tar"
    p_request.params[API_TARGET] = make_hash(str("missing"))
    p_request.params[API_TARGETS] = make_hash(str(txt_file))
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert R_ERROR in body

    # Bad target file
    p_request.params.clear()
    p_request.params[API_CMD] = "archive"
    p_request.params[API_TYPE] = "application/x-tar"
    p_request.params[API_TARGET] = make_hash(str(txt_file.parent))
    p_request.params[API_TARGETS] = make_hash(str(txt_file.parent / "missing"))
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert R_ERROR in body


def test_dim(p_request, settings, jpeg_file):
    """Test the dim command."""
    p_request.params[API_CMD] = "dim"
    # "substitute" is not supported in our backend yet. It's optional in api 2.1
    # p_request.params[API_SUBSTITUTE] = "640x480"
    p_request.params[API_TARGET] = make_hash(str(jpeg_file))
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert R_ERROR not in body
    assert body[R_DIM] == "420x420"


def test_dim_errors(p_request, settings, jpeg_file):
    """Test the dim command with errors."""
    # Invalid parameters
    p_request.params[API_CMD] = "dim"
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert body[R_ERROR] == "Invalid parameters"

    # File not found
    p_request.params.clear()
    p_request.params[API_CMD] = "dim"
    p_request.params[API_TARGET] = make_hash(str("missing"))
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert body[R_ERROR] == "File not found"

    # Access denied
    jpeg_file.chmod(0o100)  # Set execute permission only
    p_request.params.clear()
    p_request.params[API_CMD] = "dim"
    p_request.params[API_TARGET] = make_hash(str(jpeg_file))
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert body[R_ERROR] == "Access denied"

    # TODO: Add a test if the image library cannot calculate dimensions.
    # Change the code to return an error in the response first.


def test_duplicate(p_request, settings, txt_file):
    """Test the duplicate command."""
    ext = txt_file.suffix
    duplicated_file = "{} copy{}".format(txt_file.stem, ext)
    duplicated_path = txt_file.parent / duplicated_file
    p_request.params[API_CMD] = "duplicate"
    p_request.params[API_TARGETS] = make_hash(str(txt_file))
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert R_ERROR not in body
    assert R_ADDED in body
    assert body[R_ADDED][0]["hash"] == make_hash(str(duplicated_path))


def test_duplicate_errors(p_request, settings, txt_file):
    """Test the duplicate command with errors."""
    # Invalid parameters
    p_request.params[API_CMD] = "duplicate"
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert body[R_ERROR] == "Invalid parameters"

    # File not found
    p_request.params.clear()
    p_request.params[API_CMD] = "duplicate"
    p_request.params[API_TARGETS] = make_hash(str("missing"))
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert body[R_ERROR] == "File not found"

    # Access denied
    txt_file.chmod(0o100)  # Set execute permission only
    p_request.params.clear()
    p_request.params[API_CMD] = "duplicate"
    p_request.params[API_TARGETS] = make_hash(str(txt_file))
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert body[R_ERROR] == "Access denied"

    txt_file.chmod(0o400)  # Reset read permission
    current = txt_file.parent
    current.chmod(0o500)  # Set read and execute permission only
    p_request.params.clear()
    p_request.params[API_CMD] = "duplicate"
    p_request.params[API_TARGETS] = make_hash(str(txt_file))
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert body[R_ERROR] == "Access denied"

    # TODO: Add a test for when the copy action fails.


def test_extract(p_request, settings, zip_file):
    """Test the extract command."""
    p_request.params[API_CMD] = "extract"
    p_request.params[API_TARGET] = make_hash(str(zip_file))
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert R_ERROR not in body
    assert R_ADDED in body


def test_extract_errors(p_request, settings, zip_file):
    """Test the extract command with errors."""
    # Invalid parameters
    p_request.params[API_CMD] = "extract"
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert body[R_ERROR] == "Invalid parameters"

    # File not found
    p_request.params.clear()
    p_request.params[API_CMD] = "extract"
    p_request.params[API_TARGET] = make_hash(str("missing"))
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert body[R_ERROR] == "File not found"

    p_request.params.clear()
    p_request.params[API_CMD] = "extract"
    p_request.params[API_TARGET] = make_hash(str(zip_file.parent))
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert body[R_ERROR] == "File not found"

    # Access denied
    current = zip_file.parent
    current.chmod(0o500)  # Set read and execute permission only
    p_request.params.clear()
    p_request.params[API_CMD] = "extract"
    p_request.params[API_TARGET] = make_hash(str(zip_file))
    response = connector(p_request)

    assert response.status_code == 200
    body = response.json
    assert body[R_ERROR] == "Access denied"

    # TODO: Add a test for when the copy action fails.
