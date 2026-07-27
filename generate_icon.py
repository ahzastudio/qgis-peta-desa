import zlib
import struct

def generate_png(width, height, color_rgb=(0, 120, 215)):
    # PNG signature
    png = bytearray(b'\x89PNG\r\n\x1a\n')
    
    # IHDR chunk
    ihdr_data = struct.pack("!IIBBBBB", width, height, 8, 2, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data)
    png.extend(struct.pack("!I", len(ihdr_data)))
    png.extend(b'IHDR')
    png.extend(ihdr_data)
    png.extend(struct.pack("!I", ihdr_crc))

    # IDAT chunk
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0) # filter type none
        for x in range(width):
            # Draw a border and fill
            if x in (0, width-1) or y in (0, height-1):
                raw_data.extend(b'\x00\x00\x00') # Black border
            else:
                raw_data.extend(bytes(color_rgb))

    compressed = zlib.compress(raw_data)
    idat_crc = zlib.crc32(b'IDAT' + compressed)
    png.extend(struct.pack("!I", len(compressed)))
    png.extend(b'IDAT')
    png.extend(compressed)
    png.extend(struct.pack("!I", idat_crc))

    # IEND chunk
    iend_crc = zlib.crc32(b'IEND')
    png.extend(struct.pack("!I", 0))
    png.extend(b'IEND')
    png.extend(struct.pack("!I", iend_crc))

    return bytes(png)

# Save icon.png
png_bytes = generate_png(32, 32, (0, 169, 230))
with open(r"d:\TOOLBOX\TEMPLATE PETA DESA\QGIS_Plugin_Peta_Desa\icon.png", "wb") as f:
    f.write(png_bytes)

import os
target = os.path.expandvars(r"%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\Template_Peta_Desa_PerKaBIG\icon.png")
with open(target, "wb") as f:
    f.write(png_bytes)

print("icon.png generated successfully!")
