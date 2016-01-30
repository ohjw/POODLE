import web_crawler
import web_scraper
import page_rank
import search
import pickle
import sys
import os

database_built = False
poodle_data = {}

def init_menu_options():
    options = {
        '-build': build_database,
        '-restore': restore_database,
        '-exit': sys.exit
    }

    if database_built:
        options['-search'] = search_database
        options['-print'] = print_database
        options['-dump'] = dump_database

    menu(options)


def build_database():
    # https://dunluce.infc.ulst.ac.uk/d12wo/Web/B3/test_index.html
    # http://adrianmoore.net/com506/test_web/index.html
    web_crawler.get_url()  # crawl url

    # page has been crawled and scraped so set this to True to enable more options
    global database_built
    database_built = True

    # getting values for graph, index and ranks to add to the poodleData dictionary
    graph = web_crawler.get_graph()
    index = web_scraper.get_index()
    ranks = page_rank.compute_ranks(graph)

    # add all data to poodle dictionary
    poodle_data['graph'] = graph
    poodle_data['index'] = index
    poodle_data['ranks'] = ranks

    init_menu_options()


def dump_database():
    # write to produce the poodle text file
    fout = open("poodle.txt", "w")
    pickle.dump(poodle_data, fout)
    fout.close()

    print " WOOF Poodle data saved!"
    print " Saved dictionary: \n"
    print poodle_data
    init_menu_options()


def restore_database():
    # load in the 3 text files (graph, index and pageRank)
    global poodle_data
    if os.path.exists("poodle.txt"):
        fin = open("poodle.txt", "r")
        poodle_data = pickle.load(fin)
        fin.close()

        global database_built
        database_built = True

        print " WOOF! Poodle data fetched!"
        print " Dictionary found: \n"
        print poodle_data
    else:
        print " WOOF! No previous file in the database. -- Try building first.\n"

    init_menu_options()


def print_database():
    # print the 3 dictionaries (graph, index and pageRank) in poodle_data
    print " - - - - - - - Page Graph - - - - - - - \n"
    print poodle_data['graph']
    print "\n - - - - - - - Page Index - - - - - - - \n"
    print poodle_data['index']
    print "\n - - - - - - - Page Ranks - - - - - - - \n"
    print poodle_data['ranks']

    init_menu_options()


def search_database():
    # search the poodle data until prompted to end search by user
    while True:
        search.get_search_phrase(poodle_data)


def menu(options):
    while True:
        print "\n WOOF! What can Poodle do for you?\n "
        print " -build Creates the poodle database \n -restore Retrieve dump"
        if database_built:
            print " -dump Save database \n -print Print database \n -search Search the database"
        print " -exit Exit POODLE \n"

        user_option = raw_input(" Option: ")
        user_option = user_option.strip()
        user_option = user_option.lower()

        if user_option in options:
            break
        else:
            print "Invalid option entered -- Please try again. \n"

    options[user_option]()


def main():
    # displaying an image of a poodle on start
    fin = open("poodle_image.txt", "r")
    for line in fin:
        print line
    fin.close()

    init_menu_options()


if __name__ == "__main__":
    main()
