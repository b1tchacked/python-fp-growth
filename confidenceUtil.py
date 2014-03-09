__author__ = 'b1tchacked'
#Unsolved reference
def findConfidentItemSets(supportedItemSets , master, items ):

    #Function that sees whether the given support values concur with independent sets
    def isConfidentItemSet ( itemset , support , support1 , tree ):
        confidenceMeasure = 4
        combSupport = 0
        itemset.sort(key=lambda v: items[v], reverse=False)
        i = 1
        for treeNode in tree.nodes(itemset[0]):
            curSupport = treeNode.count
            cur = treeNode.parent
            while cur is not None and i < len(itemset):
                cur = cur.parent
                if  cur != None and cur.item == itemset[i]:
                    i += 1
            if i >= len(itemset):
                combSupport += curSupport

        if ( abs(combSupport - (support*support1/10)) >= confidenceMeasure ):
            print str(itemset) +  str(combSupport)
            return True
        else:
            return False
    #Look for confident itemset pairs from the supported sets
    confidentItemSets = []
     #Function used to check whether two itemsets intersection is confident
    goodPair = True
    for itemset, support in supportedItemSets:
        for itemset1, support1 in supportedItemSets:
            for item in itemset:
                for item1 in itemset1:
                    if item == item1:
                        goodPair = False
                        break
                if not goodPair:
                    break
            if goodPair:
                if isConfidentItemSet ( itemset + itemset1 , support , support1 , master ):
                    #Tuple Added to List
                    confidentItemSets.append( (itemset,itemset1 ) )

            #Bringing back to initial State for checks
            if not goodPair:
                goodPair = True
    return confidentItemSets


