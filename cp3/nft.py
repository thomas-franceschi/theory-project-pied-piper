from __future__ import print_function
import collections

def strip_comments(file):
    """Remove comments. Everything from // to the end of the line is
    considered a comment."""
    for line in file:
        try:
            i = line.index("//")
            line = line[:i]
        except ValueError:
            pass
        yield line.strip()

class NFT(object):
    """Nondeterministic finite automaton."""
    
    # This creates a mini-subclass NFT.Transition with three attributes
    Transition = collections.namedtuple('Transition', ['q', 'a', 'b', 'r'])

    # Special name for empty string
    EPSILON = '&'

    def __init__(self):
        self.states = set()        # States
        self.start = None          # Start state
        self.accept = set()        # Accept states
        self.transitions = set()   # Transitions
        self.transitions_from = {} # Transitions indexed by q
        self.transitions_on = {}   # Transitions indexed by a

    def set_start(self, q):
        """Set the start state."""
        self.states.add(int(q))
        self.start = int(q)

    def add_accept(self, q):
        """Add an accept state."""
        self.states.add(int(q))
        self.accept.add(int(q))

    def add(self, t):
        """Add a transition (of type NFT.Transition)."""
        self.states.update([int(t.q), int(t.r)])
        self.transitions.add(t)
        self.transitions_from.setdefault(t.q, set()).add(t)
        self.transitions_on.setdefault(t.a, set()).add(t)

    def add_transition(self, q, a, b, r):
        """Add a transition (specified by a 'from' state, a symbol, and a 'to'
        state)."""
        self.add(self.Transition(int(q), a, b, int(r)))

    @classmethod
    def read(cls, file):
        """Read a NFT from a file."""
        f = strip_comments(file)
        m = cls()

        # Internally, we renumber all the states. This is not so good
        # for readability but is sometimes more convenient.
        states = next(f).split()
        state_index = {q:i for (i,q) in enumerate(states)}
        _ = next(f) # ignore alphabet
        
        m.set_start(state_index[next(f)])
        for q in next(f).split(): m.add_accept(state_index[q])
        
        for line in f:
            q, a, b, r = line.split()
            m.add_transition(state_index[q], a, b, state_index[r])
        return m

    def write(self, file):
        """Write a NFT to a file."""
        file.write(' '.join(map(str, self.states)) + '\n')
        alphabet = set(t.a for t in self.transitions if t.a != self.EPSILON)
        file.write(' '.join(map(str, alphabet)) + '\n')
        file.write(str(self.start) + '\n')
        file.write(' '.join(map(str, self.accept)) + '\n')
        for t in self.transitions:
            file.write("{} {} {} {}\n".format(t.q, t.a, t.b, t.r))

    def any_path(m):
        """Returns a path from the start state to an accept state, or raises
        ValueError if there is none."""
        if m.start in m.accept: return []
        # Breadth-first search
        agenda = collections.deque()
        visited = set()
        for t in m.transitions_from.get(m.start, []):
            agenda.append([t])
            visited.add(t.r)
        while len(agenda) > 0:
            path = agenda.popleft()
            q = path[-1].r
            if q in m.accept:
                return path
            for t in m.transitions_from.get(q, []):
                if t.r not in visited:
                    agenda.append(path+[t])
                    visited.add(t.r)
        raise ValueError('no path')

    def is_empty(m):
        """Returns true iff an NFT recognizes the empty language."""
        try:
            path = m.any_path()
            return False
        except ValueError:
            return True

    @classmethod
    def singleton(cls, w):
        """Returns a NFT that recognizes {w}."""
        m = cls()
        m.set_start(0)
        for i,a in enumerate(w):
            m.add_transition(i, a, a, i+1)
        m.add_accept(len(w))
        return m

    @classmethod
    def compose(cls, m1, m2):
        """Compose two NFTs."""

        epsilon = cls.EPSILON
        # This computes the state number of a pair of state numbers q1 and q2.
        def q(q1, q2): return q1*len(m2.states)+q2
        m = cls()
        m.set_start(q(m1.start,m2.start))

        # three cases for composition
        for t1 in m1.transitions:
            for t2 in m2.transitions:
                if t1.b == t2.a:
                    m.add_transition(q(t1.q, t2.q), t1.a, t2.b, q(t1.r, t2.r))
                if t1.b == epsilon:
                    m.add_transition(q(t1.q, t2.q), t1.a, epsilon, q(t1.r, t2.q))
                    m.add_transition(q(t1.q, t2.r), t1.a, epsilon, q(t1.q, t2.r))
                if t2.a == epsilon:
                    m.add_transition(q(t1.q, t2.q), epsilon, t2.b, q(t1.q, t2.r))
                    m.add_transition(q(t1.r, t2.q), epsilon, t2.b, q(t1.r, t2.r))

        for q1 in m1.accept:
            for q2 in m2.accept:
                m.add_accept(q(q1,q2))

        return m

if __name__ == "__main__":

    filename = file('../examples/sipser-t1.nft')

    nft = NFT.read(filename)
    nft.write(file('text.txt', 'w'))