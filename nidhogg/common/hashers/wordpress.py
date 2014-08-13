import hashlib


SYMBOLS = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def encode64(raw_input, rounds):
    output = ''
    current = 0

    while current < rounds:
        value = raw_input[current]
        current += 1
        output += SYMBOLS[value & 0x3f]

        if current < rounds:
            value |= (raw_input[current] << 8)
        output += SYMBOLS[(value >> 6) & 0x3f]

        if current >= rounds:
            break

        current += 1
        if current < rounds:
            value |= (raw_input[current] << 16)

        output += SYMBOLS[(value >> 12) & 0x3f]

        if current >= rounds:
            break

        current += 1
        output += SYMBOLS[(value >> 18) & 0x3f]

    return output


def check_password(raw_password, stored_hash):
    output = '*0'

    if stored_hash.startswith(output):
        output = '*1'

    if not stored_hash.startswith('$P$') and not stored_hash.startswith('$H$'):
        return output

    symbol_place = SYMBOLS.find(stored_hash[3])
    if symbol_place < 7 or symbol_place > 30:
        return output

    count = 1 << symbol_place
    salt = stored_hash[4:12]

    if len(salt) != 8:
        return output

    sp_digest = hashlib.md5((salt + raw_password).encode()).digest()

    for i in range(count):
        sp_digest = hashlib.md5(sp_digest + raw_password.encode()).digest()

    return stored_hash[:12] + encode64(sp_digest, 16) == stored_hash
