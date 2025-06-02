<div align="center">
  <h1><b>CS2 Glow (Highlight Enemies and Teammates) 🔐</b></h1>
  <img src="images/glow.png" alt="Glow Effect" width="550">
</div>

## Requirements
- **Python Version**: 3.11.4 (recommended, as used in development)
- **Dependencies**: Install required packages using:
  ```bash
  pip install Pymem
  
## Overview
CS2 Glow is a Python-based tool that applies RGB-based glow effects to enemies and teammates in Counter-Strike 2 (CS2) by manipulating the game's memory. Teammates are highlighted with a green RGB glow (0, 255, 0), and enemies with a yellow RGB glow (255, 255, 0). This project is intended **solely for educational and research purposes** to explore game memory interactions.

## Features
- Highlights teammates with green RGB glow (0, 255, 0) and enemies with yellow RGB glow (255, 255, 0).
- Automatically detects living entities and applies glow effects.
- Configurable memory offsets via `offsets.txt`.
- Lightweight and optimized to minimize CPU usage.

## Note Guide
1. **Launch Options**:
   - Add `-insecure` to CS2’s Steam launch options:
     1. In Steam Library, right-click **Counter-Strike 2**.
     2. Go to **Properties** > **General** > **Launch Options**.
     3. Enter `-insecure`.
   - ![Launch Options Setting](images/setting.png)

2. **Dump Offsets**:
   - Run CS2 with `-insecure`, use **cs2-dumper** to dump 'offsets' and `client.dll`.
   - Or use the provided and latest updated `offsets.txt`

3. **Safety**:
   - Test in safe environment; `-insecure` disables Valve Anti-Cheat (VAC).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer
This project is intended solely for **educational and research purposes**. It provides tools and examples for understanding BitLocker encryption and decryption mechanisms. **Do not use this project for any malicious or unauthorized activities**, as such actions may violate applicable laws and regulations.

The author is not responsible for any damage, data loss, or legal consequences resulting from the use or misuse of this project. Always test and validate the code in a controlled, secure environment before applying it to critical systems. Ensure you have proper authorization and backups before performing any encryption or decryption operations.

## Donate ⭐
- **USDT (TRC-20)**: `TCLCdvvvgy6Pbj5VnTzaYBwGKzBDyBEyGL`
- **BTC**: `3EALRZzA5vp7i6kXhELTujphiJC4WwZESF`
