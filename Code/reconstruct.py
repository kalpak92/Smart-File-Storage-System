#!/usr/bin/python3
import sys

def get_data_from_metadata(data):
        word_block = data.split('-')
        #print ("WORDS:",word_block)
        res = []
        count = []
        for wordblock in word_block:
                word = wordblock.split(':')
                #print(word)
                res.append(word[0])
                count.append(word[1])
        #print (res)
        #print(count)

        wordBytes = []
        for word in res:
                wordBytes.append(word.split('+'))
        wordBytes[:-1]

        #print(wordBytes)
        #print(count)
        #print (len(wordBytes), len(count))

        return(wordBytes, count)

def reconstruct_from_metadata(filename, original_data, count_original_data):
        with open(filename,"wb") as fd:
                temp = 0
                for count in count_original_data:
                        c = int(count)
                        word_block = original_data[temp]

                        for i in range(0,c):
                                for j in word_block:
                                        data = int(j).to_bytes(1, byteorder='big')
                                        #print(data)
                                        fd.write(data)
                        temp += 1;


if __name__ == "__main__":
        try:
                with open(".metadata.txt","r") as f:
                        data = f.read().strip()

                data = data.split('$')
                filename = data[0]
                #print("File Name : ",filename)

                data_from_metadata = get_data_from_metadata(data[1])

                original_data = data_from_metadata[0]
                count_original_data = data_from_metadata[1]

                #print(original_data)
                #print(count_original_data)

                reconstruct_from_metadata(filename, original_data, count_original_data)

        except OSError as e:
                print(e)