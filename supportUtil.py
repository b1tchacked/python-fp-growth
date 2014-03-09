__author__ = 'b1tchacked'
from collections import defaultdict, namedtuple
from itertools import imap
from FpTree import FPTree
from FpNode import FPNode
itemSupport = defaultdict(lambda: 0) # mapping from items to their supports

def clean_transaction(transaction):
    transaction = filter(lambda v: v in itemSupport, transaction)
    transaction.sort(key=lambda v: itemSupport[v], reverse=True)
    return transaction

def find_with_suffix(tree, suffix,minimum_support):
    include_support = True
    for item, nodes in tree.items():
        support = sum(n.count for n in nodes)
        if support >= minimum_support and item not in suffix:
            # New winner!
            found_set = [item] + suffix
            yield (found_set, support) if include_support else found_set

            # Build a conditional tree and recursively search for frequent
            # itemsets within it.
            cond_tree = conditional_tree_from_paths(tree.prefix_paths(item),
                minimum_support)
            for s in find_with_suffix(cond_tree, found_set,minimum_support):
                yield s # pass along the good news to our caller

def conditional_tree_from_paths(paths, minimum_support):
    """Builds a conditional FP-tree from the given prefix paths."""
    tree = FPTree()
    condition_item = None
    items = set()

    # Import the nodes in the paths into the new tree. Only the counts of the
    # leaf notes matter; the remaining counts will be reconstructed from the
    # leaf counts.
    for path in paths:
        if condition_item is None:
            condition_item = path[-1].item

        point = tree.root
        for node in path:
            next_point = point.search(node.item)
            if not next_point:
                # Add a new node to the tree.
                items.add(node.item)
                count = node.count if node.item == condition_item else 0
                next_point = FPNode(tree, node.item, count)
                point.add(next_point)
                tree._update_route(next_point)
            point = next_point

    assert condition_item is not None

    # Calculate the counts of the non-leaf nodes.
    for path in tree.prefix_paths(condition_item):
        count = path[-1].count
        for node in reversed(path[:-1]):
            node._count += count

    # Eliminate the nodes for any items that are no longer frequent.
    for item in items:
        support = sum(n.count for n in tree.nodes(item))
        if support < minimum_support:
            # Doesn't make the cut anymore
            for node in tree.nodes(item):
                if node.parent is not None:
                    node.parent.remove(node)

    # Finally, remove the nodes corresponding to the item for which this
    # conditional tree was generated.
    for node in tree.nodes(condition_item):
        if node.parent is not None: # the node might already be an orphan
            node.parent.remove(node)

    return tree

def find_frequent_itemsets(transactions, minimum_support, include_support=False):
    """
    Find frequent itemsets in the given transactions using FP-growth. This
    function returns a generator instead of an eagerly-populated list of items.

    The `transactions` parameter can be any iterable of iterables of items.
    `minimum_support` should be an integer specifying the minimum number of
    occurrences of an itemset for it to be accepted.

    Each item must be hashable (i.e., it must be valid as a member of a
    dictionary or a set).

    If `include_support` is true, yield (itemset, support) pairs instead of
    just the itemsets.
    """
    processed_transactions = []
    global itemSupport
    # Load the passed-in transactions and count the support that individual
    # items have.
    for transaction in transactions:
        processed = []
        for item in transaction:
            itemSupport[item] += 1
            processed.append(item)
        processed_transactions.append(processed)

    # Remove infrequent items from the item support dictionary.
    itemSupport = dict((item, support) for item, support in itemSupport.iteritems()
        if support >= minimum_support)

    # Build our FP-tree. Before any transactions can be added to the tree, they
    # must be stripped of infrequent items and their surviving items must be
    # sorted in decreasing order of frequency.

    master = FPTree()
    #Runs clean_transaction on every processed_transactions and returns as a tuple
    for transaction in imap(clean_transaction, processed_transactions):
        master.add(transaction)

    #Can Further Check for Confidence Values
    supportedItemSets = []
    for itemset in find_with_suffix(master, [], minimum_support):
        supportedItemSets.append(itemset)

    return supportedItemSets,master,itemSupport