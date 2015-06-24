import data_processing.top_songs as top_songs
import os
import configs
import numpy
from scipy.sparse import dok_matrix
import math


def run(log_dirpath, song_list_filepath, write_filepath):
    song_indices = top_songs.read_song_list(song_list_filepath)
    counts = {}

    for filename in os.listdir(log_dirpath):
        print "Reading " + filename
        with open(log_dirpath + filename) as log_file:
            for line in log_file:
                parts = line.strip().split(' ')
                song_id, user_id, count = int(parts[2]), parts[1], int(parts[0])
                if song_id in song_indices:
                    counts[(song_id, user_id)] = counts.get((song_id, user_id), 0) + count

    user_counts = {}
    for (song_id, user_id), count in counts.iteritems():
        if user_id in user_counts:
            user_counts[user_id].append((song_id, count))
        else:
            user_counts[user_id] = [(song_id, count)]

    num_users_filtered = 0
    with open(write_filepath, 'w') as write_file:
        for count_list in user_counts.itervalues():
            if len(count_list) < 8:
                num_users_filtered += 1
                continue

            write_file.write(' '.join(str(song_id) + ',' + str(count) for song_id, count in count_list) + '\n')

    print "Users filtered = ", num_users_filtered


def read_docs(docs_filepath, song_list_filepath):
    song_indices = top_songs.read_song_list(song_list_filepath)
    matrix = dok_matrix((50000, top_songs.NUM_SONGS), numpy.float16)     # 456883
    user_index = 0

    with open(docs_filepath) as docs_file:
        for line in docs_file:
            counts = get_counts(song_indices, line)
            if len(counts) >= 10:
                for song_index, count in counts:
                    matrix[user_index, song_index] = count
                user_index += 1
                if user_index == 50000:
                    return matrix

    return matrix


def get_counts(song_indices, line):
    counts = []

    for song_count_str in line.rstrip().split(' '):
        parts = [int(x) for x in song_count_str.split(',')]
        if parts[0] in song_indices:
            counts.append((song_indices[parts[0]], 4.6 * math.log(1 + parts[1])))

    return counts


def check():
    max_counts = []
    with open(configs.PROCESSED_USER_DATA + "all.txt") as f:
        for line in f:
            counts = line.rstrip().split(' ')
            max_counts.append(sorted((int(pair.split(',')[1]) for pair in counts), reverse=True)[:5])
    print '\n'.join([str(x) for x in sorted(enumerate(max_counts), key=lambda pair: pair[1], reverse=True)[:1000]])


if __name__ == '__main__':
    #run(configs.RAW_USER_DATA, configs.USER_DATA + "chosen_songs.txt", configs.PROCESSED_USER_DATA + "all.txt")
    read_docs(configs.PROCESSED_USER_DATA + "all.txt", configs.USER_DATA + "chosen_songs.txt")