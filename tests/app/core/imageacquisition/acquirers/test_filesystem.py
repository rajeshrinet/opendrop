import math
from pathlib import Path
from unittest.mock import patch, Mock

import numpy as np
import pytest

from opendrop.app.core.imageacquisition.acquirers.filesystem import (
    _load_image,
    FilesystemAcquirer,
    UnknownImageTypeError,
    EmptyPathsError,
)

PARENT_DIR = Path(__file__).parent


def test_FilesystemAcquirer_init_with_empty_image_paths_raises_error():
    with pytest.raises(EmptyPathsError):
        FilesystemAcquirer(image_paths=(), frame_interval=1)


@pytest.mark.parametrize('invalid_value', (-1, math.nan, math.inf))
def test_FilesystemAcquirer_init_with_invalid_frame_interval_raises_error(invalid_value: float):
    with patch('opendrop.app.core.imageacquisition.acquirers.filesystem._load_image'):
        with pytest.raises(ValueError):
            FilesystemAcquirer(image_paths=('image1', 'image2'), frame_interval=invalid_value)


@pytest.mark.parametrize('invalid_value', (-1, math.nan, math.inf))
def test_FilesystemAcquirer_init_with_single_image_path_ignores_invalid_frame_interval(invalid_value: float):
    with patch('opendrop.app.core.imageacquisition.acquirers.filesystem._load_image'):
        FilesystemAcquirer(image_paths=('image1',), frame_interval=invalid_value)


def test_FilesystemAcquirer_images():
    mock_images = [Mock(), Mock(), Mock(), Mock(), Mock()]
    image_paths = ['1', '2', '3']
    with patch('opendrop.app.core.imageacquisition.acquirers.filesystem._load_image', side_effect=mock_images):
        acquirer = FilesystemAcquirer(image_paths=image_paths, frame_interval=1)
        assert acquirer.images == mock_images[:len(image_paths)]


def test_FilesystemAcquirer_frame_interval():
    with patch('opendrop.app.core.imageacquisition.acquirers.filesystem._load_image'):
        acquirer = FilesystemAcquirer(image_paths=('1', '2', '3'), frame_interval=123)
        assert acquirer.frame_interval == 123


def test_load_image_with_sample_image():
    image = _load_image(PARENT_DIR / 'astronaut.jpg')
    expect = np.load(PARENT_DIR / 'astronaut.npy')
    assert np.allclose(image, expect, atol=5.0)


def test_load_image_with_nonexistent_path():
    with pytest.raises(FileNotFoundError):
        _load_image(PARENT_DIR / 'this-file-does-not-exist.png')


def test_load_image_with_unknown_file_type():
    with pytest.raises(UnknownImageTypeError):
        _load_image(PARENT_DIR / 'random')
