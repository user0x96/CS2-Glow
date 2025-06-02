#Copyright 2025 © @user0x96
#Github: https://github.com/user0x96
#Donate⭐ 
#+USDT(TRC-20): TCLCdvvvgy6Pbj5VnTzaYBwGKzBDyBEyGL
#+BTC: 3EALRZzA5vp7i6kXhELTujphiJC4WwZESF
import time
from typing import Tuple, List
from pymem import Pymem
from pymem.exception import MemoryReadError, MemoryWriteError

class Vector4:
    def __init__(self, x: float, y: float, z: float, w: float):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

class Cs2Memory:
    def __init__(self, processName: str = "cs2.exe"):
        self.pm = Pymem(processName)
    
    # ====================== Read pointer from memory ====================
    def readPointer(self, address: int, offset: int) -> int:
        """Reads a pointer from the specified address with an offset."""
        try:
            return self.pm.read_ulonglong(address + offset)
        except MemoryReadError:
            return 0
    
    # ====================== Read pointer chain ====================
    def readPointerChain(self, address: int, offsets: List[int]) -> int:
        """Reads a pointer through a chain of offsets."""
        pointer = address
        for offset in offsets:
            pointer = self.readPointer(pointer, offset)
            if pointer == 0:
                break
        return pointer
    
    # ====================== Read integer ====================
    def readInteger(self, address: int, offset: int) -> int:
        """Reads an integer from the specified address with an offset."""
        try:
            return self.pm.read_int(address + offset)
        except MemoryReadError:
            return 0
    
    # ====================== Read unsigned integer ====================
    def readUnsignedInteger(self, address: int, offset: int) -> int:
        """Reads an unsigned integer from the specified address with an offset."""
        try:
            return self.pm.read_uint(address + offset)
        except MemoryReadError:
            return 0
    
    # ====================== Write unsigned integer ====================
    def writeUnsignedInteger(self, address: int, value: int) -> bool:
        """Writes an unsigned integer to the specified address."""
        try:
            self.pm.write_uint(address, value)
            return True
        except MemoryWriteError:
            return False

class Offsets:
    localPlayerPawn = 0x18540D0  # dwLocalPlayerPawn (offsets)
    entityList = 0x19FFE48      # dwEntityList  (offsets)
    playerPawnHandle = 0x824     # m_hPlayerPawn (client.dll)
    teamNumber = 0x3E3          # m_iTeamNum (client.dll)
    lifeState = 0x348           # m_lifeState (client.dll)
    glowBase = 0xC00            # m_Glow (client.dll)
    glowColorOverride = 0x40 # m_glowColorOverride (client.dll)
    glowing = 0x51 # m_bGlowing (client.dll)
    #Note: Replace the latest offsets here with the available tool or update offset directly from my project offsets.txt
    #Github: https://github.com/a2x/cs2-dumper

# ====================== Update glow effect ====================
def updateGlowEffect(cs2Memory: Cs2Memory, client: int):
    """Applies glow effect to entities based on team status."""
    # Get local player
    currentPlayer = cs2Memory.readPointer(client, Offsets.localPlayerPawn)
    
    if currentPlayer == 0:  # Exit if player not found
        return
    
    # Get entity list
    entityList = cs2Memory.readPointer(client, Offsets.entityList)
    if entityList == 0:  # Exit if entity list not found
        return
    
    for i in range(64):  # Loop through max 64 entities
        entry = cs2Memory.readPointer(entityList, 0x10)
        if entry == 0:
            continue
        
        currentController = cs2Memory.readPointer(entry, i * 0x78)
        if currentController == 0:
            continue
        
        # Get current pawn
        pawnHandle = cs2Memory.readInteger(currentController, Offsets.playerPawnHandle)
        if pawnHandle == 0:
            continue
        
        # Calculate entry2 and currentPawn
        entry2 = cs2Memory.readPointer(entityList, 0x8 * ((pawnHandle & 0x7FFF) >> 9) + 0x10)
        currentPawn = cs2Memory.readPointer(entry2, 0x78 * (pawnHandle & 0x1FF))
        
        if currentPawn == 0:  # Skip if pawn not found
            continue
        
        if currentPawn == currentPlayer:  # Skip self
            continue
        
        lifeState = cs2Memory.readUnsignedInteger(currentPawn, Offsets.lifeState)
        
        if lifeState != 256:  # Skip if entity is not alive
            continue
        
        # Determine if entity is teammate or enemy
        isTeammate = cs2Memory.readInteger(currentPawn, Offsets.teamNumber) == \
                     cs2Memory.readInteger(currentPlayer, Offsets.teamNumber)
        
        # Set glow color
        glowColor = Vector4(0.0, 1.0, 0.0, 1.0) if isTeammate else Vector4(1.0, 1.0, 0.0, 1.0)
        
        # Update glow effect
        colorAddress = currentPawn + Offsets.glowBase + Offsets.glowColorOverride
        glowAddress = currentPawn + Offsets.glowBase + Offsets.glowing
        
        color = Color()
        color.argb = convertToArgb(glowColor)
        cs2Memory.writeUnsignedInteger(colorAddress, color.argb)
        cs2Memory.writeUnsignedInteger(glowAddress, 1)

# ====================== Convert color to ARGB ====================
def convertToArgb(color: Vector4) -> int:
    """Converts Vector4 color to ARGB integer."""
    # Calculate RGB values
    r = int(min(max(color.x, 0.0), 1.0) * 255)  # Red
    g = int(min(max(color.y, 0.0), 1.0) * 255)  # Green
    b = int(min(max(color.z, 0.0), 1.0) * 255)  # Blue
    a = int(min(max(color.w, 0.0), 1.0) * 255)  # Alpha
    
    # Return ARGB color code
    return (a << 24) | (r << 16) | (g << 8) | b

class Color:
    def __init__(self):
        self.argb = 0

# ====================== Main function ====================
def pain() -> None:
    """Main function to initialize and run the glow effect loop."""
    # Initialize objects and variables
    cs2Memory = Cs2Memory("cs2.exe")
    try:
        client = None
        for module in cs2Memory.pm.list_modules():
            if module.name.lower() == "client.dll":
                client = module.lpBaseOfDll
                break
        if client is None:
            raise Exception("Could not find client.dll in cs2.exe process")
    except Exception as e:
        print(f"Failed to get client.dll address: {e}")
        exit(1)

    # Main loop
    while True:
        updateGlowEffect(cs2Memory, client)
        time.sleep(0.001)  # Reduce CPU usage

if __name__ == "__main__":
    pain()