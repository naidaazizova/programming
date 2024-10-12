def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATT ACKATDAWN", "LEMON")
    'LXF OPVEFRNHR'
    """
    ciphertext = ""
    keyword = keyword.upper()
    keyword_length = len(keyword)
    keyword_space = 0
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            shift = ord(keyword[(i - keyword_space)  % keyword_length]) - ord('A')
            if plaintext[i].islower():
                encrypted_char = chr((ord(plaintext[i]) - ord('a') + shift) % 26 + ord('a'))
            else:
                encrypted_char = chr((ord(plaintext[i]) - ord('A') + shift) % 26 + ord('A'))

            ciphertext += encrypted_char
        else:
            ciphertext += plaintext[i]
            keyword_space += 1
    return ciphertext

def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXF OPVEFRNHR", "LEMON")
    'ATT ACKATDAWN'
    """
    plaintext = ""
    keyword = keyword.upper()
    keyword_length = len(keyword)
    keyword_space = 0
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            shift = ord(keyword[(i - keyword_space)  % keyword_length]) - ord('A')
            if ciphertext[i].islower():
                decrypted_char = chr((ord(ciphertext[i]) - ord('a') - shift + 26) % 26 + ord('a'))
            else:
                decrypted_char = chr((ord(ciphertext[i]) - ord('A') - shift - 26) % 26 + ord('A'))
            plaintext += decrypted_char
        else:
            plaintext += ciphertext[i]
            keyword_space += 1
    return plaintext