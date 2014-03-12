# encoding: utf-8

"""
A Python implementation of the FP-growth algorithm.

Basic usage of the module is very simple:

    >>> from fp_growth import find_frequent_itemsets
    >>> find_frequent_itemsets(transactions, minimum_support)
"""
from collections import defaultdict, namedtuple
from itertools import imap

__author__ = 'Eric Naeseth <eric@naeseth.com>'
__coAuthor__ = 'b1tchacked'
__copyright__ = 'Copyright © 2009 Eric Naeseth'
__license__ = 'MIT License'


from confidenceUtil import findConfidentItemSets
from supportUtil import findFrequentOredItemSets
from supportUtil import  find_frequent_itemsets

#Testing Code Should be removed
def printTreeBranches(node):
    print str(node.item) + " " + str(node.branchNos) + " " +str(node.count)
    for child in node.children:
        printTreeBranches(child)

if __name__ == '__main__':
    from optparse import OptionParser
    import csv

    p = OptionParser(usage='%prog data_file')
    p.add_option('-s', '--minimum-support', dest='minsup', type='int',
        help='Minimum itemset support (default: 2)')
    p.set_defaults(minsup=2)

    options, args = p.parse_args()
    if len(args) < 1:
        p.error('must provide the path to a CSV file to read')

    f = open(args[0])
    try:
        supportedItemSets,master,itemSupport = find_frequent_itemsets(csv.reader(f), options.minsup, True)
        findFrequentOredItemSets( master , options.minsup )
        """print "Minimum Supported Sets"
        for pair,support in supportedItemSets:
            print str(pair) + " " + str(support)

        print "Printing Tree"
        printTreeBranches(master.root)"""

        print "Confident Sets"
        for pair in findConfidentItemSets( supportedItemSets , master , itemSupport ):
            print str(pair[0]) + " " + str(pair[1])
    finally:
        f.close()
