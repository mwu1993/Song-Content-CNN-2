import song_docs
import configs
import multiprocessing
import data_processing.top_songs as top_songs
from plsa import pLSA, loglikelihood


def train(docs_filepath, song_list_filepath, write_filepath, n_topics):
    m = song_docs.read_docs(docs_filepath, song_list_filepath)

    for n_its in [50, 100, 200, 400]:
        p = pLSA()
        p.average_train(3)(m, n_topics, n_its)
        print loglikelihood(m, p.p_z, p.p_w_z, p.p_d_z)
    return

    with open(write_filepath, 'w') as write_file:
        write_file.write("LLH: " + str(l.loglikelihood()) + '\n')
        write_file.write("Topic dist: " + ','.join(str(x) for x in l.nz_) + '\n')
        for i in range(top_songs.NUM_SONGS):
            write_file.write(','.join(str(row[i]) for row in l.topic_word_) + '\n')


if __name__ == '__main__':
    #m = song_docs.read_docs(configs.PROCESSED_USER_DATA + "all.txt", configs.USER_DATA + "chosen_songs.txt")
    train(configs.PROCESSED_USER_DATA + "all.txt", configs.USER_DATA + "chosen_songs.txt", "", 10)