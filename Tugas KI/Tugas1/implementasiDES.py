# Konversi HEX ke biner
def hex_to_bin(hex_str):
    return bin(int(hex_str, 16))[2:].zfill(64)

# Konversi biner ke HEX
def bin_to_hex(bin_str):
    return hex(int(bin_str, 2))[2:].zfill(16)

# Tabel permutasi awal (Initial Permutation IP)
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# Tabel Inverse Initial Permutation (IP-1)
IP_inv = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]

# Fungsi untuk melakukan permutasi
def permute(input_bits, perm_table):
    return ''.join(input_bits[i-1] for i in perm_table)

# Tabel permutasi kompresi PC-1 (64-bit jadi 56-bit)
PC_1 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

# Tabel kompresi kunci PC-2 (56-bit jadi 48-bit)
PC_2 = [14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32]

# Tabel pergeseran bit pada kunci
shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# Ekspansi (R) 32-bit ke 48-bit
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

# Fungsi SBox (Substitusi)
S_BOX = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 6, 8, 0, 15, 9, 14, 12, 3, 5],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6]],

    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 14, 1, 7, 6, 11, 0, 8, 13]],

    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 5, 2, 12, 6, 10, 15, 14, 3, 8],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 1, 3, 14, 10, 4, 9, 11, 2, 12, 5, 0, 15, 13, 7, 8]],

    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 6, 3, 11, 5]]
]

# Fungsi untuk melakukan substitusi S-Box
def s_box_substitution(input_bits):
    output_bits = ''
    for i in range(8):
        # Ambil 6 bit
        chunk = input_bits[i*6:(i+1)*6]
        row = int(chunk[0] + chunk[5], 2)  # baris
        col = int(chunk[1:5], 2)          # kolom
        output_bits += bin(S_BOX[i][row][col])[2:].zfill(4)  # ambil dari S-Box
    return output_bits

# Fungsi untuk menghitung F(K, R)
def f_function(R, K):
    R_expanded = permute(R, E)  # Ekspansi R
    R_xor_K = bin(int(R_expanded, 2) ^ int(K, 2))[2:].zfill(48)  # XOR dengan kunci
    S_output = s_box_substitution(R_xor_K)  # Substitusi S-Box
    # Permutasi P
    P = [16, 7, 20, 21, 29, 12, 28, 17,
         1, 15, 23, 26, 5, 18, 31, 10,
         2, 8, 24, 14, 32, 27, 3, 9,
         19, 13, 30, 6, 22, 11, 4, 25]
    return permute(S_output, P)

# Fungsi untuk menggeser kunci
def shift_key(key, shift_count):
    return key[shift_count:] + key[:shift_count]

# Fungsi untuk menghasilkan kunci untuk 16 ronde
def generate_keys(key):
    key = permute(key, PC_1)  # Kompresi kunci
    C, D = key[:28], key[28:]  # Pisahkan ke C dan D
    keys = []
    for i in range(16):
        C = shift_key(C, shift_table[i])  # Geser C
        D = shift_key(D, shift_table[i])  # Geser D
        keys.append(permute(C + D, PC_2))  # Kompresi kunci
    return keys

# Fungsi DES
def des_encrypt(plain_text, key):
    plain_text_bits = permute(hex_to_bin(plain_text), IP)  # Permutasi awal
    left, right = plain_text_bits[:32], plain_text_bits[32:]  # Pisahkan ke L dan R
    keys = generate_keys(hex_to_bin(key))  # Hasilkan kunci
    for i in range(16):
        temp = right
        right = bin(int(left, 2) ^ int(f_function(right, keys[i]), 2))[2:].zfill(32)  # L = L XOR f(R, K)
        left = temp  # Simpan nilai R ke L
    combined = right + left  # Gabungkan R dan L
    return bin_to_hex(permute(combined, IP_inv))  # Kembalikan ke HEX

# Fungsi untuk mendekripsi
def des_decrypt(cipher_text, key):
    cipher_text_bits = permute(hex_to_bin(cipher_text), IP)  # Permutasi awal
    left, right = cipher_text_bits[:32], cipher_text_bits[32:]  # Pisahkan ke L dan R
    keys = generate_keys(hex_to_bin(key))  # Hasilkan kunci
    for i in range(15, -1, -1):  # Dekripsi dengan kunci terbalik
        temp = right
        right = bin(int(left, 2) ^ int(f_function(right, keys[i]), 2))[2:].zfill(32)  # L = L XOR f(R, K)
        left = temp  # Simpan nilai R ke L
    combined = right + left  # Gabungkan R dan L
    return bin_to_hex(permute(combined, IP_inv))  # Kembalikan ke HEX

# Contoh penggunaan
if __name__ == "__main__":
    plaintext = "0123456789ABCDEF"
    key = "133457799BBCDFF1"
    
    # Enkripsi
    cipher_text = des_encrypt(plaintext, key)2
    print(f"Cipher Text: {cipher_text}")
    
    # Dekripsi
    decrypted_text = des_decrypt(cipher_text, key)
    print(f"Decrypted Text: {decrypted_text}")
