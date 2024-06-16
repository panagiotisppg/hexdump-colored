import sys

# Settings
SHOW_VALUES = True      # Whether to show the hex value inside each color block
SHOW_SPACING = False    # Whether to have blank spacing between the colors
BOX_WIDTH = 4           # Width of the color box

def contrast_color(color):
    if color < 16:
        return 15 if color == 0 else 0

    if color > 231:
        return 15 if color < 244 else 0

    g = ((color - 16) % 36) // 6
    return 0 if g > 2 else 15

def print_color_block(value):
    contrast = contrast_color(value)
    if SHOW_VALUES:
        hex_str = f"{value:02x}"
        print(f"\033[48;5;{value}m\033[38;5;{contrast}m {hex_str} \033[0m", end=' ' if SHOW_SPACING else '')
    else:
        print(f"\033[48;5;{value}m{' ' * BOX_WIDTH}\033[0m", end=' ' if SHOW_SPACING else '')

def print_file_contents_colored(file_path):
    try:
        with open(file_path, 'rb') as f:
            byte = f.read(16)
            addr = 0
            while byte:
                # print the address in hexadecimal format
                print(f"{addr:08x}  ", end='')
                addr += 16
                
                # Print each byte in hexadecimal format
                for i, b in enumerate(byte):
                    value = b
                    print_color_block(value)
                    if i == 7:
                        print('  ', end='')
                
                # fill in missing bytes to align with the next line
                if len(byte) < 16:
                    print("    "*(15-i)+'  ', end = '')
                
                # ASCII representation of the bytes
                print(' |', end='')
                for b in byte:
                    if 32 <= b < 127:  # printable ASCII range
                        print(chr(b), end='')
                    else:
                        print('.', end='')
                print('|')
                
                byte = f.read(16)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 colorize_binary.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    print_file_contents_colored(file_path)
