import os
import sys
script_path = os.path.dirname(os.path.abspath(__file__))
film_dir = script_path+'/'+sys.argv[1]
genre = ['comedy', 'action', 'horror', 'thriller', 'adventure', 'soap', 'drama', 'family', 'fantasy']
for fname in os.listdir(film_dir):
    for other_genre in genre:    
        if other_genre == sys.argv[1].lower():
            continue
        if other_genre in fname.lower() :
           file_dir = film_dir+'/'+fname
           moved_dir = script_path+'/deleted/'+fname
           os.rename(file_dir, moved_dir)
           print("File " + fname + "has been MOVED")

