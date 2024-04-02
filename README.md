# Network Scanner

- A Python-based network scanner.

## Code Comparison: v0.1 vs v0.2 vs v0.3

| Feature              | v0.1                          | v0.2                                         | v0.3                                         |
|----------------------|-------------------------------|----------------------------------------------|----------------------------------------------|
| Imports              | socket, re, ipaddress        | socket, re, ipaddress                       | socket, re, ipaddress, ThreadPoolExecutor   |
| IP Validation        | Custom regex pattern         | Custom regex pattern                        | Built-in IP address validation              |
| Port Range Validation| Custom regex pattern         | Custom regex pattern                        | Built-in port range validation              |
| Scan Function        | Single function `scan`       | Split into `scan_ports` functions           | Split into `scan_ports` functions           |
| Concurrent Scanning  | Not implemented              | ThreadPoolExecutor                          | ThreadPoolExecutor                          |
| Error Handling       | Basic checks                 | Basic error checks                          | Enhanced error handling                     |
| Scan Output          | Prints open ports            | Prints open ports                           | Prints open ports with detailed error msgs  |
| Modular Structure    | Functions grouped in main    | Functions organized into separate tasks     | Functions organized into separate tasks     |

## v0.3

### **Improvements**

1. Enhanced IP and port range validation.
2. Improved error handling with detailed error messages.
3. Modularized code for better organization.

## v0.2

### Features

- Scans single devices or entire networks.
- Concurrent port scanning using ThreadPoolExecutor.

### Known Issues

- Basic IP and port range validation.
- Limited error handling capabilities.

## v0.1

### Features

- Port scanning for a single device.
- Port scanning for a network of devices.

### Issues

- Incorrectly identifies some valid IP addresses as invalid.
- Sluggish performance due to sequential execution.

## Future Plans

- Consider integrating additional features such as service detection.
