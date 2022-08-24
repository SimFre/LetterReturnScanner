# Letter Return Scanner
Scan QR-codes with a barcode scanner and send the data to SFTP

This will read the serial port of a Honeywell Genesis 7580g barcode scanner, that is set to continous reading QR-codes off of envelopes. The QR data is written into text files and periodically uploaded to an SFTP server, where a backend service will parse and handle the data.

The script runs headless with Systemd on a Raspberry Pi.
