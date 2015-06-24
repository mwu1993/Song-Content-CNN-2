import configs
import os


NUM_SONGS = 6000


def get_song_count(user_dirpath, cutoff=1):
    counts = {}
    users = set()
    listens = 0

    for filename in os.listdir(user_dirpath):
        print "Reading " + filename
        with open(user_dirpath + filename) as user_file:
            for line in user_file:
                parts = line.strip().split(' ')
                song_id, user_id, count = int(parts[2]), parts[1], int(parts[0])
                counts[(song_id, user_id)] = counts.get((song_id, user_id), 0) + count
                users.add(user_id)
                listens += int(parts[0])

    print "Num songs = ", len(counts)
    print "Num users = ", len(users)
    print "Num listens = ", listens

    counts_by_song = {}
    for (song_id, user_id), count in counts.iteritems():
        if count >= cutoff:
            counts_by_song[song_id] = counts_by_song.get(song_id, 0) + 1

    return sorted(counts_by_song.items(), key=lambda pair: pair[1], reverse=True)


def write_song_counts(user_dirpath, write_filepath, cutoff=1):
    counts = get_song_count(user_dirpath, cutoff)
    with open(write_filepath, 'w') as write_file:
        for song_id, count in counts:
            write_file.write(str(song_id) + ',' + str(count) + '\n')


def write_song_list(song_counts_filepath, song_list_filepath):
    with open(song_counts_filepath) as song_file:
        with open(song_list_filepath, 'w') as output:
            for i in range(NUM_SONGS):
                output.write(song_file.readline().split(',')[0] + '\n')


def read_song_list(song_list_filepath):
    song_indices = {}

    with open(song_list_filepath) as song_list:
        for i in range(NUM_SONGS):
            line = song_list.readline()
            song_indices[int(line.strip())] = len(song_indices)

    return song_indices

if __name__ == '__main__':
    #for cutoff in [5]:
    #    write_song_counts(configs.RAW_USER_DATA, configs.USER_DATA + "top_songs" + str(cutoff) + ".txt", cutoff)

    write_song_list(configs.USER_DATA + "top_songs.txt", configs.USER_DATA + "chosen_songs.txt")