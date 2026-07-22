from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from src.utils.config import get_project_root


DATASETS_ROOT = get_project_root() / "data" / "datasets"


def get_dataset_path(dataset_name: str) -> Path:
    return DATASETS_ROOT / dataset_name


def is_google_drive_folder(url: str) -> bool:
    return "drive.google.com" in url and "folders" in url


def download_google_drive_folder(url: str, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    try:
        import gdown
    except ImportError:
        raise ImportError(
            "gdown is required to download Google Drive folders. Install it with `pip install gdown`."
        )

    if destination.exists() and any(destination.iterdir()):
        return

    if "drive.google.com/drive/folders/" not in url:
        raise ValueError("Unsupported Google Drive URL format. Use a folder share URL.")

    folder_id = url.split("folders/")[-1].split("?")[0]
    if not folder_id:
        raise ValueError("Could not parse Google Drive folder ID from URL")
    gdown.download_folder(url, output=str(destination), quiet=False, use_cookies=False)


def ensure_dataset(dataset_name: str, local_path: Path | None = None, source_url: str | None = None) -> Path:
    target_path = get_dataset_path(dataset_name)
    if target_path.exists() and any(target_path.iterdir()):
        return target_path

    if local_path is not None and local_path.exists():
        if local_path.is_dir():
            shutil.copytree(local_path, target_path, dirs_exist_ok=True)
            return target_path
        raise ValueError(f"Local dataset path is not a directory: {local_path}")

    if source_url is not None:
        if is_google_drive_folder(source_url):
            download_google_drive_folder(source_url, target_path)
            return target_path

        raise ValueError("Unsupported dataset source URL. Only Google Drive folder links are supported.")

    raise FileNotFoundError(
        f"Dataset {dataset_name} not available locally and no source URL provided."
    )


def locate_files(dataset_path: Path, suffix: str = ".csv") -> list[Path]:
    return [path for path in dataset_path.rglob(f"*{suffix}") if path.is_file()]
