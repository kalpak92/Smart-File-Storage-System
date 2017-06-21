#!/usr/bin/python3
import sys
import itertools

def cmp(a, b):
    return (a > b) - (a < b)

def metadata_to_string(metadata, file_name):
        meta_string = file_name+"$"

        for i in metadata:
                data_block = i[0]
                data_block_count = i[1]
                #print (b, c)
                for j in data_block:
                        meta_string += str(j)+"+"

                meta_string = meta_string[:-1] + ":"
                meta_string += str(data_block_count) + "-"

        return (meta_string[:-1])

def make_metadata(data_samples, file_name):
        count = 1
        prev = []
        metadata = []

        for blockdata in data_samples:
                if cmp(blockdata, prev) != 0:
                        if prev:
                                entry = (prev,count)
                                metadata.append(entry)
                        count = 1
                        prev = blockdata
                else:
                        count += 1
        else:
                entry = (blockdata, count)
                metadata.append(entry)

        meta_string = metadata_to_string(metadata, file_name)

        return meta_string

def compress(filename, data, block_size):
        data_samples = []
        count = 0
        block_sized_data = []
        for b in data:
                if count < block_size:
                        #print(type(b))
                        block_sized_data.append(b)
                        #print(block_sized_data)
                        count += 1
                else:
                        data_samples.append(block_sized_data)
                        count = 1
                        block_sized_data = [b]
        else:
                data_samples.append(block_sized_data)

        #print(data_samples)
        #print ("Original Size ",len(data_samples))

        compressed_data_samples = list(data_samples for data_samples,_ in itertools.groupby(data_samples))
        #print (compressed_data_samples)
        #print ("Compressed Size ",len(compressed_data_samples))

        print (len(compressed_data_samples))

        metadata = make_metadata(data_samples, file_name)

        #print (metadata)

        with open(".metadata.txt", "w") as fd:
                fd.write("%s\n" % metadata)
        write_compressed_data(filename, compressed_data_samples)

def write_compressed_data(filename, compressed_data):

        with open(filename,"wb") as f:
                for data_blocks in compressed_data:
                        for data in data_blocks:
                                #print(type(data))
                                temp = data.to_bytes(1, byteorder='big')
                                #print(type(temp))
                                #print(temp)
                                f.write(temp)


if __name__ == "__main__":
        file_name = sys.argv[1]
        block_size = int(sys.argv[2])

        #print(file_name, block_size)

        try:
                with open(file_name, "rb") as f:
                        data = f.read()

                compress(file_name, data, block_size)
        except OSError as e:
                print(e)
