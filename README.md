Python library for postcard scanner

# Installation
Installation manual is for linux, tested on Raspberry Pi (Raspberry Pi OS, bullseye, Release date: January 28th 2022)
- Install Python >=3.5.
- Install python venv
    ```
    sudo apt-get install python3-venv
    ```
- Create and activate virtual environment
    ```
    source venv/bin/activate
    python3 -m venv venv
    ```
- Clone this repo
    ```
    git clone https://github.com/nzottmann/postcardscanner.git
    ```
- Install `postcardscanner`
    ```
    pip install -e postcardscanner
    ```
- Run example
    ```
    cd postcardscanner/examples
    python scanner_demo.py
    ```
    Output:
    ```
    DEBUG:postcardscanner:state: enabled
    Received image
    DEBUG:postcardscanner:state: scanning
    DEBUG:postcardscanner:state: enabled
    ```
    `img.jpg` is now a copy of `example.jpg`
    

# Usage
Examples in `examples` folder show how to use this library.

## Examples

### scanner_v0.py
Example for using the first hardware prototype, v0

### scanner_demo_camera.py
Example for testing without scanner hardware, but with pi camera. Captures images from camera.

### scanner_demo.py
Example for testing without hardware. Input own image for testing or use `example.jpg`.
