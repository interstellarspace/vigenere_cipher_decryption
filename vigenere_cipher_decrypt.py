#!/usr/bin/python
import math

CONST_LET_PROB = [0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.020, 0.061, 0.070, 0.002, 0.008, 0.040, 0.024,
                  0.067, 0.075, 0.019, 0.001, 0.060, 0.063, 0.091, 0.028, 0.010, 0.023, 0.001, 0.020, 0.001 ]

'''Read text from the file'''
def read_text_from_file(filename):
    f = open(filename,'r')
    text = f.readlines()
    text = "".join(text)
    return text.strip()

'''Transform text into array'''
def text_to_list(text):
    l = list(text)
    return l

'''Print array into regular string'''
def print_list(l):
    print(''.join(l))

'''Get int value of a letter'''
def let_int(letter):
    return ord(letter)


class Datagram_Freq:
    letter = ''
    freq = 0
    percent = 0
    locs = list()
    def __init__(self, l, f, p, loc):
        self.letter = l
        self.freq = f
        self.percent = p
        self.locs = loc

class Text_Frequencies:
    cipher = ''
    clean_cipher = ''
    current_freq_list = list()

    def __init__(self, name_or_text, filenameYes):
        if filenameYes :
            self.cipher = read_text_from_file(name_or_text)
            t = self.cipher.lower()
            t = t.replace(" ","")
            t = t.replace('\n',"")
            t = t.replace('\t',"")
            self.clean_cipher = t
            current_freq_list = list()
            print("Using filename: " + name_or_text)
        else:
            self.cipher = name_or_text
            t = name_or_text
            t = t.replace(" ","")
            t = t.replace('\n',"")
            t = t.replace('\t',"")
            self.clean_cipher = t
            current_freq_list = list()
        
        
    def get_datagram_frequencies(self, length):         #ASCII [0 to 255]
        t = self.cipher.lower()                         #A = 65 Z = 90
        t = t.replace(" ","")
        t = t.replace('\n',"")
        t = t.replace('\t',"")
        freq_list = list()                              #a = 97 z = 122
        gram_list = list()
        gram_freq_list = list()
        loc_list = list()
        
        i = 0
        while (i + length) <= len(t):
            curr_gram = t[i:i+length]
            if curr_gram not in gram_list:
                gram_list.append(curr_gram)
                freq_list.append(0)
                loc_list.append(list())
            ind = gram_list.index(curr_gram,)
            loc_list[ind].append(i+1)
            freq_list[ind] += 1
            i += 1
        assert(len(freq_list)==len(gram_list))
        for l in gram_list:
            ind2 = gram_list.index(l,)
            gram_freq_list.append(Datagram_Freq(l, freq_list[ind2],
                                                     float(freq_list[ind2])/sum(freq_list),loc_list[ind2]))
        gram_freq_list = sorted(gram_freq_list, key=lambda Datagram_Freq: Datagram_Freq.letter, reverse=False)
        self.current_freq_list = gram_freq_list
        #self.print_frequencies()
        return gram_freq_list
    

    def print_frequencies(self):
        num_sum = 0
        per_sum = 0
        print("Ciphertext:\n" + self.cipher)
        print("\n\tFREQUENCIES/ANALYSIS")
        for data in self.current_freq_list:
            num_sum += data.freq
            per_sum += data.percent
            i_x = int(data.percent*100)
            print(data.letter + ": " + str(data.freq) + " " + "{0:.2f}%".format(data.percent*100) 
                  + "\t" + "x"*i_x*2 + "\t\t" + str(data.locs))
        print("Sum of frequencies: " + str(num_sum))
        print("Sum of percentage: " + "{0:.0f}%\n".format(per_sum*100))
        
class Vigenere_Cipher:
    txt_freq = None
    
    def __init__(self, filename):
        self.txt_freq = Text_Frequencies(filename, 1)
        print("CIPHERTEXT:\n" + self.txt_freq.cipher + "\n")
        
    def get_index_coin(self, m):
        substr_list = list()
        for i in range(0, m):
            substr = self.get_vig_substring(i, m)
            #print("Vigenere substring: start position: " + str(i) + ", m = " + str(m))
            #print("Substring: " + substr)
            ioc = self.get_ind_coin_subs(substr)
            print("Vigenere substring: position: " + str(i) + ",\tm = " + str(m) + "\t\tIOC = " + "%.3f" % ioc)
            substr_list.append(substr)
        print("")
        return substr_list
        
    def get_ind_coin_subs(self, substr):
        i_of_co = 0.00
        txt_freq_subs = Text_Frequencies(substr,0)
        gram_list = txt_freq_subs.get_datagram_frequencies(1)
        for gram in gram_list :
            i_of_co += (gram.freq * (gram.freq - 1.0)) / (len(substr) * (len(substr)-1.0))
        return i_of_co
        #print("Index of coincidence:" + str("%.3f" % i_of_co) + "\n")
    
    def get_vig_substring(self, i, m):
        substr = self.txt_freq.clean_cipher[i::m]
        return(substr)
    
    def decrypt_vig(self, key):
        decrypted = list()
        cipher = self.txt_freq.clean_cipher
        pointer_key = 0
        for l in cipher:
            d = ord(l) - ord(key[pointer_key])
            d = d %26
            d = chr(d+97)
            decrypted.append(d)
            pointer_key += 1
            if pointer_key >= len(key):
                pointer_key = 0
        return decrypted


def print_ind_coin_Q1(filename):
    ciphertext = Vigenere_Cipher(filename)
    for i in range(0,6) :
        ciphertext.get_index_coin(i)

def print_ind_coin_Q2(filename):
    ciphertext = Vigenere_Cipher(filename)
    for i in range(0,10) :
        ciphertext.get_index_coin(i)
    print("Correct key length: m = 6")
    substr_list = ciphertext.get_index_coin(6)
    print("Substrings: m = 6")
    print("[1]" + substr_list[0])
    print("[2]" + substr_list[1])
    print("[3]" + substr_list[2])
    print("[4]" + substr_list[3])
    print("[5]" + substr_list[4])
    print("[6]" + substr_list[5] + "\n\n")
    key = print_mtable(substr_list)
    return(ciphertext, key)
        
def print_mtable(substr_list):
    key = list()
    print("Mutual indices of coincidence:")
    for substr in substr_list:
        curr_substr = Text_Frequencies(substr,0)
        print("Subtext: " + curr_substr.clean_cipher)
        freq_list = curr_substr.get_datagram_frequencies(1)
        freq_list = transform(freq_list)
        for i in range(0,26):
            mg = 0.0
            for g in range(0,26):
                p = CONST_LET_PROB[g]
                n = len(substr)
                f = freq_list[(g+i)%26]
                mg += p * f
            mg = mg / n
            if mg >= 0.059:
                print(str(chr(97+i)) + "\t" + "%.3f"%mg + " <==== " + chr(97+i))
                key.append(chr(97+i))
            else:
                print(str(chr(97+i)) + "\t" + "%.3f"%mg)
        print("")
    return(key)
            
def transform(freq_list):
    freqs = [0]*26
    for f in freq_list:
        int_eqv = ord(f.letter) % 97
        freqs[int_eqv] = 0.00 + f.freq
    return(freqs)