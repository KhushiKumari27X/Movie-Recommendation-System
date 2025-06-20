import pickle
import gzip
with open("similarity.pkl","rb")as f_in:
    data=pickle.load(f_in)
with gzip.open("similarity_compressed.pkl.gz","wb")as f_out:
     pickle.dump(data,f_out)
print("Compression done!")