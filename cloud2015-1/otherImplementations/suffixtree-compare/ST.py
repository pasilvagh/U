import time, sys, os
import readFromFile
#URL: http://nbviewer.ipython.org/gist/BenLangmead/6796858

# Suffix tree built with simple O(m^2)-time algorithm.
class SuffixTree(object):
    
    class Node(object):
        def __init__(self, depth, off, ln, lab=None):
            self.depth = depth
            self.off = off # offset into T of substring
            self.ln = ln   # length of substring
            self.out = {}  # outgoing edges; maps characters to nodes
    
    def __init__(self, t):
        """ Make suffix tree, without suffix links, from s in quadratic time
            and linear space """
        t += '$'
        self.t = t
        self.root = self.Node(0, 0, 0, None)
        self.root.out[t[0]] = self.Node(len(t), 0, len(t), t)
        self.nodes = []
        for i in xrange(1, len(t)):
            cur = self.root
            j = i
            while j < len(t):
                if t[j] in cur.out:
                    child = cur.out[t[j]]
                    lab = t[child.off:child.off+child.ln]
                    k = j+1 # Walk along edge
                    while k-j < len(lab) and t[k] == lab[k-j]:
                        k += 1
                    if k-j == len(lab):
                        cur = child # exhausted the edge
                        j = k
                    else:
                        # fell off in middle of edge
                        cExist, cNew = lab[k-j], t[k]
                        mid = self.Node(cur.depth + k-j, child.off, k-j, lab[:k-j])
                        mid.out[cNew] = self.Node(mid.depth + len(t[k:]), k, len(t[k:]), t[k:])
                        self.nodes.append(mid)
                        self.nodes.append(mid.out[cNew])
                        mid.out[cExist] = child
                        child.off += (k-j)
                        child.ln -= (k-j)
                        cur.out[t[j]] = mid
                else:
                    # Create a new edge hanging off of this node
                    cur.out[t[j]] = self.Node(cur.depth + len(t[j:]), j, len(t[j:]), t[j:])
                    self.nodes.append(cur.out[t[j]])
    
    def saLcp(self):
        # Return suffix array and an LCP1 array corresponding to this
        # suffix tree.  self.root is root, self.t is the text.
        self.minSinceLeaf = 0
        sa, lcp1 = [], []
        def __visit(n):
            if len(n.out) == 0:
                # leaf node, record offset and LCP1 with previous leaf
                sa.append(len(self.t) - n.depth)
                lcp1.append(self.minSinceLeaf)
                # reset LCP1 to depth of this leaf
                self.minSinceLeaf = n.depth
            # visit children in lexicographical order
            for c, child in sorted(n.out.iteritems()):
                __visit(child)
                # after each child visit, perhaps decrease
                # minimum-depth-since-last-leaf value
                self.minSinceLeaf = min(self.minSinceLeaf, n.depth)
        __visit(self.root)
        return sa, lcp1[1:]

if len(sys.argv) < 2:
	sys.exit('Usage: %s input-file' % sys.argv[0])
if not os.path.exists(sys.argv[1]):
	sys.exit('ERROR: input-file %s was not found!' % sys.argv[1])
else:
	_input = str(sys.argv[1])
	(S,n) = readFromFile.read(_input)
	time1 = time.clock()
	st = SuffixTree(S)
	sa, lcp1 = st.saLcp()	
	print("time: ",time.clock()-time1)
	print("SA: ", sa)
	

