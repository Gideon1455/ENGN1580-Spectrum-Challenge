def generate_codeword(entry):
    entry = str(bin(entry))
    entry = "000" + entry[2:]
    entry_array = []
    for el in entry: entry_array.append(el)
    print(entry_array)
    codeword = []
    for i in range(256):
        thirty_first_bit = int(entry_array[30])
        twenty_eighth_bit = int(entry_array[27])
        codeword.append(thirty_first_bit)
        xor = twenty_eighth_bit ^ thirty_first_bit
        entry_array.pop()
        entry_array.insert(0, str(xor))
    print(codeword)


generate_codeword(140256304)
