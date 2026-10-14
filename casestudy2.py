import random
import sys
import time

class DenseAdjacencyMatrix:
    def __init__(self, n_users):
        self.n = n_users
        self.matrix = [bytearray(n_users) for _ in range(n_users)]  
    def add_friendship(self, a, b):
        if a == b:
            return
        self.matrix[a][b] = 1
        self.matrix[b][a] = 1          

    def remove_friendship(self, a, b):
        self.matrix[a][b] = 0
        self.matrix[b][a] = 0

    def are_friends(self, a, b):
        return self.matrix[a][b] == 1

    def friends_of(self, a):
        return [i for i, v in enumerate(self.matrix[a]) if v]    

    def print_matrix(self, names=None):
        names = names or [str(i) for i in range(self.n)]
        print("     " + " ".join(f"{nm[:3]:>3}" for nm in names))
        for i, row in enumerate(self.matrix):
            print(f"{names[i][:3]:>4} " + " ".join(f"{v:>3}" for v in row))

class SparseAdjacencyMatrix:
    def __init__(self, n_users):
        self.n = n_users
        self.rows = {}                 
        self.edge_count = 0

    def _check(self, u):
        if not 0 <= u < self.n:
            raise IndexError(f"user id {u} out of range 0..{self.n - 1}")

    def add_friendship(self, a, b):
        self._check(a); self._check(b)
        if a == b:
            return False
        row_a = self.rows.setdefault(a, set())
        if b in row_a:
            return False               
        row_a.add(b)
        self.rows.setdefault(b, set()).add(a)    
        self.edge_count += 1
        return True

    def remove_friendship(self, a, b):
        if b in self.rows.get(a, ()):
            self.rows[a].discard(b)
            self.rows[b].discard(a)
            self.edge_count -= 1

    def are_friends(self, a, b):                 
        return b in self.rows.get(a, ())

    def friends_of(self, a):                     
        return self.rows.get(a, set())

    def degree(self, a):
        return len(self.rows.get(a, ()))

    def mutual_friends(self, a, b):
        return self.friends_of(a) & self.friends_of(b)      

    def suggest_friends(self, a, top_k=5):
        
        mine = self.friends_of(a)
        score = {}
        for f in mine:
            for fof in self.friends_of(f):
                if fof != a and fof not in mine:
                    score[fof] = score.get(fof, 0) + 1
        ranked = sorted(score.items(), key=lambda kv: (-kv[1], kv[0]))
        return ranked[:top_k]

    def average_degree(self):
        return 2 * self.edge_count / self.n if self.n else 0

def human(nbytes):
    for unit in ("B", "KB", "MB", "GB", "TB", "PB"):
        if nbytes < 1024:
            return f"{nbytes:,.1f} {unit}"
        nbytes /= 1024
    return f"{nbytes:,.1f} EB"


def memory_report(sizes, avg_friends=200):
    print(f"{'Users':>16} | {'Dense (1 bit/cell)':>20} | {'Sparse (~8 B/edge end)':>24}")
    print("-" * 68)
    for n in sizes:
        dense_bits = n * n / 8                      
        sparse = n * avg_friends * 8                
        print(f"{n:>16,} | {human(dense_bits):>20} | {human(sparse):>24}")

def small_demo():
    print("=" * 68)
    print("PART 1: Small network - dense adjacency matrix")
    print("=" * 68)
    names = ["Asha", "Ravi", "Meera", "Karan", "Neha"]
    net = DenseAdjacencyMatrix(len(names))
    for a, b in [(0, 1), (0, 2), (1, 2), (1, 3), (3, 4)]:
        net.add_friendship(a, b)
    net.print_matrix(names)
    print("\nAre Asha and Ravi friends?  ", net.are_friends(0, 1))
    print("Are Asha and Karan friends? ", net.are_friends(0, 3))
    print("Ravi's friends:", [names[i] for i in net.friends_of(1)])


def large_demo(n_users=1_000_000, avg_friends=8, seed=42):
    print("\n" + "=" * 68)
    print(f"PART 2: {n_users:,} users - sparse adjacency matrix")
    print("=" * 68)
    random.seed(seed)
    net = SparseAdjacencyMatrix(n_users)

    t0 = time.time()
    target_edges = n_users * avg_friends // 2
    while net.edge_count < target_edges:
        net.add_friendship(random.randrange(n_users), random.randrange(n_users))
    print(f"Built {net.edge_count:,} friendships in {time.time() - t0:.1f}s "
          f"(average {net.average_degree():.1f} friends per user)")

    user = 12345
    other = next(iter(net.friends_of(user)))
    print(f"\nUser {user} has {net.degree(user)} friends")
    print(f"Are {user} and {other} friends?         {net.are_friends(user, other)}")
    print(f"Are {user} and 999,999 friends?        {net.are_friends(user, 999_999)}")
    print(f"Mutual friends of {user} and {other}:     {sorted(net.mutual_friends(user, other))}")
    print(f"Suggestions for {user} (id, mutual friends): {net.suggest_friends(user)}")

    py_bytes = sys.getsizeof(net.rows) + sum(sys.getsizeof(s) for s in net.rows.values())
    print(f"\nApprox. memory used by sparse structure: {human(py_bytes)}")
    print(f"Dense matrix would need (1 bit/cell):     {human(n_users * n_users / 8)}")
if __name__ == "__main__":
    small_demo()
    print("\n" + "=" * 68)
    print("Memory: dense vs sparse (average 200 friends per user)")
    print("=" * 68)
    memory_report([1_000, 100_000, 1_000_000, 100_000_000, 1_000_000_000])
    large_demo()