from setuptools import setup, find_packages

setup(
    name='usb-hawkeye',
    version='0.1.0',
    description='Real-time USB cybersecurity monitoring and defense tool',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.15.0',
        'wmi>=1.5.1',
        'pyclamd>=0.4.0',
        'ipinfo>=4.2.2',
        'twilio>=7.0.0',
        'pandas>=1.3.0',
        'openpyxl>=3.0.0',
    ],
)
# For PyInstaller packaging, run:
#   pyinstaller --onefile --windowed main.py
