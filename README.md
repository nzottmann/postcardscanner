Python app for postcard scanner

Licensed under the [EUPL-1.2-or-later](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)

- Hardware: https://github.com/nzottmann/postcardscanner-hardware
- Python module: https://github.com/nzottmann/postcardscanner-python

# Installation
Installation manual is for Raspberry Pi OS, bullseye, Release date: 2022-09-22, tested on Pi4
- Clone this repo and install requirements in a venv
    ```
    sudo apt-get install python3-venv
    git clone https://github.com/nzottmann/postcardscanner.git
    cd postcardscanner
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
- Test with
    ```
    cd app
    python3 -m uvicorn main:app --host 0.0.0.0
    ```
- Install and start systemd service
    ```
    sudo cp postcardscanner.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable postcardscanner.service
    sudo systemctl start postcardscanner.service
    ```
- Check systemd service state
    ```
    sudo systemctl status postcardscanner.service
    sudo journalctl -u postcardscanner.service
    ```

:point_up: Adjust paths in `postcardscanner.service` if cloning to other path than `/home/pi`

:point_up: Make sure `app/main.py` uses the scanner version matching your hardware revision