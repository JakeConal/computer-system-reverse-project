import sys

def get_result(name: str) -> int:
    result = 0
    alpha_chars = [ch for ch in name if ch.isalpha()][:5]  # Keep only first 5 letters
    for ch in alpha_chars:
        index = ord(ch.lower()) - ord('a')
        result *= 26
        result += index
    return result

def get_hash(ch: str, shift: int) -> int:
    # Find the original index of the character in the HASHMAP
    original_index = HASHMAP.index(ch)

    # Calculate the new index based on the shift (simulating rotation)
    rotated_index = (original_index - shift * 6) % len(HASHMAP)
    
    return rotated_index

# Get the hash key from the rotated HASHMAP
# based on the index and shift value
def get_hash_key(index: int, shift: int) -> str:
    # Get the character from the HASHMAP based on the index and shift
    rotated_index = (index + shift * 6) % len(HASHMAP)
    return HASHMAP[rotated_index]

def convert(arr, shift):
    esp_10 = 0  # Simulate [esp+10]
    
    for ch in reversed(arr):  # ← RIGHT TO LEFT!
        if ch not in HASHMAP:
            raise ValueError(f"Character {ch} not found in rotated HASHMAP.")

        ecx = get_hash(ch,shift)            # Step 0: index of character
        edx = esp_10                        # Step 1: load current [esp+10]
        edx = edx * 9                       # Step 2: edx = edx * 9
        ecx = ecx + edx * 4                 # Step 3: ecx = ecx + edx * 4
        esp_10 = ecx                        # Step 4: write back to [esp+10]

    return esp_10

# Custom HASHMAP
HASHMAP = [
    'A', 'G', 'M', 'S', 'Y', '4', 'B', 'H',
    'N', 'T', 'Z', '5', 'C', 'I', 'O', 'U',
    '0', '6', 'D', 'J', 'P', 'V', '1', '7',
    'E', 'K', 'Q', 'W', '2', '8', 'F', 'L',
    'R', 'X', '3', '9'
]



# Get serial 5 characters "XXXXX", default is "AAAAA"
def get_key_part(serial: str, index:int, shift:int, result: int) -> str:
    if (index == -1):
        return ''.join(serial)

    # Check if "XXXXX" hashvalue > result, ex: "AAAAA"
    # Save index of the indexed character
    for i in range(36):
        # Get first index+1 characters of the serial
        # and replace the indexed character with the current character
        text = list(serial)
        text[index] = get_hash_key(i, shift)
        
        temp = convert(text, shift)
        if temp > result:
            serial[index] = get_hash_key(i-1, shift)
            break
        elif temp == result:
            serial[index] = get_hash_key(i, shift)
            break
        
    # Recursion for remaning characters
    return get_key_part(serial, index-1, shift, result)

def get_key(result: int) -> str:
    serial = ['A' for i in range(23)]  # Start with "AAAAA"
    for i in range(3):
        serial[i*6+5] = '-'
        
    # Get the key part from the result
    for i in range(4):
        temp = [get_hash_key(0, i) for j in range(5)]  # Start with "AAAAA";
        temp = get_key_part(temp, 4, i, result)
        serial[i*6:i*6+5] = temp[:5]
    
    return ''.join(serial)

def save_key(name:str, key: str) -> None:
    with open("key.txt", "w") as f:
        f.write("Name: " + name + "\n")
        f.write("Serial code: " + key)

if __name__ == "__main__":
    name = input("Enter your name: ").upper()
    print("Your name is:", name)

    result = get_result(name)
    if result < 24:
        print("THE ENTERED NAME IS NOT VALID: This name is a joke...")
        exit(0)

    print("Converted value of name:", result)
    
    license_key = get_key(result)
    print("Found matching license key:", license_key)
    
    save_key(name, license_key)
    print("License key saved to key.txt")
