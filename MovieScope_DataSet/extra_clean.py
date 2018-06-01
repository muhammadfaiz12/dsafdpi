import os
import sys

def extract_capital_word(judul):
    hasil = ""
    words = judul.split(' ')
    for word in words:
        if any(c.islower() for c in word):
            continue
        elif len(word) > 0 and not word[0].isalnum():
            continue
        else:
            hasil = hasil + " " + word

    idx = hasil.find('.')
    hasil = hasil[idx+1:]
    return hasil
  
script_path = os.path.dirname(os.path.abspath(__file__))
film_dir = script_path+'/'+sys.argv[1]
genre = ['comedy', 'action', 'romance', 'horror', 'thriller', 'adventure', 'soap', 'drama', 'family', 'fantasy']
pelem = set()
dup_counter = 0
mov_counter = 0
for fname in os.listdir(film_dir):
    title = extract_capital_word(fname)
    if(title in pelem):
        #print(title + " is Duplicate")
        dup_counter+=1
        continue
    moved = False
    for other_genre in genre:    
        if other_genre == sys.argv[1].lower():
            continue
        if other_genre in fname.lower() :
           file_dir = film_dir+'/'+fname
           moved_dir = script_path+'/deleted/'+fname
           os.rename(file_dir, moved_dir)
           print("File " + fname + " has been MOVED")
           moved = True
           mov_counter+=1
    if not moved:
        pelem.add(title)

print("DUPLICATE : " + str(dup_counter))
print("MOVED : " + str(mov_counter))
