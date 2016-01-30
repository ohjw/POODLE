import pickle
import re
import poodle

def get_user_search():
    # retrieving user input
    while True:
        user_search = raw_input(" \n What would you like to search for? (-end to exit search)\n")
        if len(user_search) > 0:
            if user_search == "-end":
                poodle.database_built = True
                poodle.init_menu_options()
            else:
                break

        else:
            print " Nothing to search for -- Try again. \n"

    # get all words from search phrase and add to a list and make it lower case
    user_search_list = re.findall(r"[\w']+", user_search.lower())

    return user_search_list


class scraped_page_info:
    # page, rank, unique words, word positions, page found on
    def __init__(self, url, rank, unique_words_count, word_positions, word_found):
        self.url = url
        self.rank = rank
        self.unique_words_count = unique_words_count
        self.word_positions = word_positions
        self.words_found = [word_found, ]

    def get_url(self):
        return self.url

    def get_rank(self):
        return self.rank

    def get_unique_words_count(self):
        return self.unique_words_count

    def get_word_positions(self):
        return self.word_positions

    def get_words_found(self):
        return self.words_found

    def adding_search_word(self, search_word, word_positions):
        self.word_positions.extend(word_positions)
        self.words_found.append(search_word)
        self.unique_words_count += 1


def finding_matches(url_data):
    # Lists to find find matches
    matched_sentences = []
    matched_words_in_page = []
    single_words_in_page = []

    for url in url_data:
        page_info = url_data[url]
        if page_info.get_unique_words_count() > 1:

            RANGE_MAX = 4

            # check the range to make sure they are a sentence
            word_found_pos = page_info.get_word_positions()
            sum_of_positions = 0

            for position in word_found_pos:
                sum_of_positions += position

            average = sum_of_positions / page_info.get_unique_words_count()

            for position in word_found_pos:
                word_range = [abs(average - position)]

            sentence_matching = True

            for range_value in word_range:
                if range_value < RANGE_MAX:
                    sentence_matching = False

            if sentence_matching:
                matched_sentences.append((page_info.get_url(), page_info.get_rank(), page_info.get_words_found()))

            else:
                matched_words_in_page.append((page_info.get_url(), page_info.get_rank(), page_info.get_words_found()))

        elif page_info.get_unique_words_count() == 1:
            single_words_in_page.append((page_info.get_url(), page_info.get_rank(), page_info.get_words_found()))

    matched_sentences = sorted(matched_sentences, reverse=True, key=lambda x: x[1])  # sort by rank which is key 1
    matched_words_in_page = sorted(matched_words_in_page, reverse=True, key=lambda x: x[1])
    single_words_in_page = sorted(single_words_in_page, reverse=True, key=lambda x: x[1])

    results = matched_sentences
    results.extend(matched_words_in_page)
    results.extend(single_words_in_page)

    return results


def get_search_phrase(poodle_data):
    user_query_list = get_user_search()
    url_data = {}

    index = poodle_data['index']
    rank = poodle_data['ranks']

    for search_word in user_query_list:

        if search_word in index:
            inner_dict = index[search_word]

            for url in inner_dict:
                word_positions = inner_dict[url]
                page_rank = rank[url]

                if url in url_data:
                    # handle if already present
                    page_info = url_data[url]
                    page_info.adding_search_word(search_word, word_positions)

                else:
                    page_info = scraped_page_info(url, page_rank, 1, word_positions, search_word)
                    url_data[url] = page_info

    results = finding_matches(url_data)

    # print the results
    if len(results) > 0:
        if len(results) == 1:
            print "\n WOOF! ", len(results), "result found!\n"
        else:
            print "\n WOOF! ", len(results), "results found!\n"
        for result in results:
            print(" URL: %s \n Words Found: %s \n Rank: %s " % (result[0], result[2], result[1]))
    else:
        print " No results found."
