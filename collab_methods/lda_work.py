import lda
import song_docs
import configs
import multiprocessing
import data_processing.top_songs as top_songs


def train(docs_filepath, song_list_filepath, write_filepath, n_topics, alpha, eta):
    m = song_docs.read_docs(docs_filepath, song_list_filepath)
    raw_input("aoue")
    l = lda.LDA(n_topics, alpha=alpha, eta=eta, n_iter=200)
    l.fit(m)
    with open(write_filepath, 'w') as write_file:
        write_file.write("LLH: " + str(l.loglikelihood()) + '\n')
        write_file.write("Topic dist: " + ','.join(str(x) for x in l.nz_) + '\n')
        for i in range(top_songs.NUM_SONGS):
            write_file.write(','.join(str(row[i]) for row in l.topic_word_) + '\n')


def exp():
    ps = []
    for n_topics in [10]:
        for alpha in [.05]:
            for eta in [.01]:
                p = multiprocessing.Process(target=train, args=(configs.PROCESSED_USER_DATA + "all.txt", configs.USER_DATA + "chosen_songs.txt",
                                                                configs.LDA + 'bbb' + str(n_topics) + '_' + str(alpha) + '_' + str(eta) + '.txt', n_topics, alpha, eta))
                p.start()
                ps.append(p)
    for p in ps:
        p.join()



if __name__ == '__main__':
    #m = song_docs.read_docs(configs.PROCESSED_USER_DATA + "all.txt", configs.USER_DATA + "chosen_songs.txt")
    train(configs.PROCESSED_USER_DATA + "all.txt", configs.USER_DATA + "chosen_songs.txt",
          configs.LDA + 'big_10_.05_.01.txt', 10, .05, .01)