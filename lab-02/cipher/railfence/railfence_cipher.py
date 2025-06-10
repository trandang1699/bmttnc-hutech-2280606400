class RailFenceCipher:
    def __init__(self):
       pass

    def rail_fence_encrypt(self, plain_text, num_rails):
        if not isinstance(plain_text, str) or not plain_text:
            raise ValueError("Plain text must be a non-empty string.")
        if not isinstance(num_rails, int) or num_rails < 2:
            raise ValueError("Number of rails must be an integer greater than or equal to 2.")

        # Create a list of lists to represent the rails
        rails = [[] for _ in range(num_rails)]
        rail_index = 0
        direction = 1  # 1 for moving down, -1 for moving up

        for char in plain_text:
            rails[rail_index].append(char)
            # Change direction at the top or bottom rail
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction
        
        # Join characters in each rail, then join the rails
        cipher_text = ''.join(''.join(rail) for rail in rails)
        return cipher_text

    def rail_fence_decrypt(self, cipher_text, num_rails):
        if not isinstance(cipher_text, str) or not cipher_text:
            raise ValueError("Cipher text must be a non-empty string.")
        if not isinstance(num_rails, int) or num_rails < 2:
            raise ValueError("Number of rails must be an integer greater than or equal to 2.")
        if num_rails > len(cipher_text):
             # If rails are more than characters, it means some rails would be empty,
             # which is typically not useful for this cipher and might indicate bad input.
             # Or it could simply mean the plaintext is shorter than num_rails.
             # We can allow this, but it's good to consider constraints.
             # For simplicity, let's allow it as the algorithm should handle it.
             pass


        # 1. Simulate the encryption path to find out the length of each rail
        # This is crucial for correctly segmenting the cipher_text back into rails.
        temp_rails = [[] for _ in range(num_rails)]
        rail_index = 0
        direction = 1
        
        for _ in range(len(cipher_text)):
            temp_rails[rail_index].append(None) 
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        rail_lengths = [len(rail) for rail in temp_rails]
        
        actual_rails = []
        current_index = 0
        for length in rail_lengths:
            actual_rails.append(list(cipher_text[current_index : current_index + length]))
            current_index += length

        plain_text_chars = []
        rail_index = 0
        direction = 1
        
        read_indices = [0] * num_rails 

        for _ in range(len(cipher_text)):

            plain_text_chars.append(actual_rails[rail_index][read_indices[rail_index]])
            read_indices[rail_index] += 1

            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction
            
        plain_text = ''.join(plain_text_chars)
        return plain_text


if __name__ == "__main__":
    cipher = RailFenceCipher()

    plain1 = "WEAREDISCOVEREDFLEEATONCE"
    key1 = 3
    encrypted1 = cipher.rail_fence_encrypt(plain1, key1)
    print(f"Plain Text: '{plain1}'")
    print(f"Key: {key1}")
    print(f"Encrypted: '{encrypted1}'") 

    decrypted1 = cipher.rail_fence_decrypt(encrypted1, key1)
    print(f"Decrypted: '{decrypted1}'")
    assert decrypted1 == plain1.upper() 

    plain2 = "HELLO WORLD"
    key2 = 4
    encrypted2 = cipher.rail_fence_encrypt(plain2, key2)
    print(f"\nPlain Text: '{plain2}'")
    print(f"Key: {key2}")
    print(f"Encrypted: '{encrypted2}'")

    decrypted2 = cipher.rail_fence_decrypt(encrypted2, key2)
    print(f"Decrypted: '{decrypted2}'")
    assert decrypted2 == plain2.upper()

    plain3 = "CRYPTOGRAPHY"
    key3 = 5
    encrypted3 = cipher.rail_fence_encrypt(plain3, key3)
    print(f"\nPlain Text: '{plain3}'")
    print(f"Key: {key3}")
    print(f"Encrypted: '{encrypted3}'")

    decrypted3 = cipher.rail_fence_decrypt(encrypted3, key3)
    print(f"Decrypted: '{decrypted3}'")
    assert decrypted3 == plain3.upper()


    try:
        cipher.rail_fence_encrypt("TEST", 1)
    except ValueError as e:
        print(f"\nError: {e}") 

    try:
        cipher.rail_fence_decrypt("TEST", 0)
    except ValueError as e:
        print(f"Error: {e}") 
    plain4 = "SHORT"
    key4 = 10 
    encrypted4 = cipher.rail_fence_encrypt(plain4, key4)
    print(f"\nPlain Text: '{plain4}'")
    print(f"Key: {key4}")
    print(f"Encrypted: '{encrypted4}'")
    decrypted4 = cipher.rail_fence_decrypt(encrypted4, key4)
    print(f"Decrypted: '{decrypted4}'")
    assert decrypted4 == plain4.upper() 