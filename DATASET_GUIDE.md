# DATASET_GUIDE

## Supported Dataset

This repository is configured to use the CICIDS2017 dataset.

## Dataset Location

Place the dataset under:

```
data/datasets/CICIDS2017/
```

## Automatic Download

The project supports Google Drive shared folder URLs via `src/utils/dataset.py`.

Example:

```bash
python training/train_behavior_model.py --gdrive-url "https://drive.google.com/drive/folders/1s3DdK5p-tNkYU9HP3b9UNepD3lorA1PX?usp=drive_link"
```

If the dataset is already present locally, pass `--local-path`:

```bash
python training/train_behavior_model.py --local-path /path/to/CICIDS2017
```

## Dataset Preparation

The training scripts currently use placeholder synthetic loaders but are designed to accept the dataset path and the following workflow:

1. Download or copy the dataset into `data/datasets/CICIDS2017/`.
2. The loader verifies presence and populates training dataset paths.
3. Training scripts automatically detect existing datasets and only download if missing.

## Notes

- `gdown` is required for Google Drive download support.
- The repository does not commit CICIDS2017 data.
- Model training is kept offline from runtime; no training occurs during API or dashboard execution.
