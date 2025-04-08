def keygen3(name: str) -> str:
    if len(name) <= 4:
        return "Name too short"

    ascii_sum = sum(ord(char) for char in name)
    suffix = ((ord(name[0]) * ord(name[-1])) ** 2) ^ 0xB221
    prefix = suffix // ((len(name)**3) ^ ascii_sum)

    return f"{prefix}-{suffix}"

if __name__ == "__main__":
    name = input("Enter a name: ")  
    result = keygen3(name)  
    print(f"Generated key: {result}")  