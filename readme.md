# Python CRUD Application

This repository contains a simple command-line CRUD application in `app.py` that stores records in `data.json`.

## Run

1. Make sure Python 3 is installed.
2. Run:

```bash
python3 app.py
```

## Actions

- List records
- Create record
- Read record
- Update record
- Delete record

Records are saved locally in `data.json`.

## QR Code Generator

A second script, `qr_generator.py`, creates a QR code from any URL or text.

Install dependencies and run:

```bash
pip install qrcode[pil]
python3 qr_generator.py
```

