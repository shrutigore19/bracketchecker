import heapq
from collections import deque
class CityMap:
    def __init__(self):
        self.roads = {}          

    def add_road(self, a, b, km):
        self.roads.setdefault(a, {})[b] = km
        self.roads.setdefault(b, {})[a] = km      

    def close_road(self, a, b):
        self.roads[a].pop(b, None)
        self.roads[b].pop(a, None)

    def shortest_route(self, start, goal):
        dist = {place: float("inf") for place in self.roads}
        came_from = {}
        dist[start] = 0
        queue = [(0, start)]                     

        while queue:
            d, place = heapq.heappop(queue)       
            if place == goal:
                break
            if d > dist[place]:                   
                continue
            for nxt, km in self.roads[place].items():
                new_d = d + km
                if new_d < dist[nxt]:             
                    dist[nxt] = new_d
                    came_from[nxt] = place
                    heapq.heappush(queue, (new_d, nxt))

        if dist[goal] == float("inf"):
            return None, None                     
        return self._build_path(came_from, start, goal), dist[goal]

    def fewest_stops_route(self, start, goal):
        came_from = {start: None}
        queue = deque([start])
        while queue:
            place = queue.popleft()
            if place == goal:
                break
            for nxt in self.roads[place]:
                if nxt not in came_from:
                    came_from[nxt] = place
                    queue.append(nxt)
        if goal not in came_from:
            return None, None
        path = self._build_path(came_from, start, goal)
        km = sum(self.roads[path[i]][path[i + 1]] for i in range(len(path) - 1))
        return path, km

    def minimum_road_network(self, start):
        visited = {start}
        chosen = []
        total = 0
        queue = [(km, start, nxt) for nxt, km in self.roads[start].items()]
        heapq.heapify(queue)
        while queue and len(visited) < len(self.roads):
            km, a, b = heapq.heappop(queue)       
            if b in visited:
                continue
            visited.add(b)
            chosen.append((a, b, km))
            total += km
            for nxt, w in self.roads[b].items():
                if nxt not in visited:
                    heapq.heappush(queue, (w, b, nxt))
        return chosen, total

    @staticmethod
    def _build_path(came_from, start, goal):
        path = [goal]
        while path[-1] != start:
            path.append(came_from[path[-1]])
        return path[::-1]


def show_route(title, path, km):
    print(f"\n{title}")
    if path is None:
        print("  No route found!")
    else:
        print("  Route   :", " -> ".join(path))
        print(f"  Distance: {km} km   |   Road segments: {len(path) - 1}")


def build_sample_city():
    city = CityMap()
    roads = [
        ("Station", "Market", 2), ("Station", "College", 5),
        ("Market", "College", 2), ("Market", "Hospital", 6),
        ("College", "Hospital", 3), ("College", "Mall", 7),
        ("Hospital", "Airport", 4), ("Mall", "Airport", 3),
        ("Mall", "Park", 2), ("Airport", "Park", 6),
        ("Station", "Bus Stand", 3), ("Bus Stand", "Mall", 10),
    ]
    for a, b, km in roads:
        city.add_road(a, b, km)
    return city


def main():
    city = build_sample_city()
    start, goal = "Station", "Airport"

    print("CITY MAP (place: neighbours with km)")
    for place, nbrs in city.roads.items():
        print(f"  {place:<10}: {nbrs}")

    path, km = city.shortest_route(start, goal)
    show_route(f"1. SHORTEST route ({start} to {goal}) - Dijkstra", path, km)

    path, km = city.fewest_stops_route(start, goal)
    show_route(f"2. FEWEST road segments ({start} to {goal}) - BFS", path, km)

    roads, total = city.minimum_road_network(start)
    print("\n3. MINIMUM roads needed to connect every place - Prim")
    for a, b, w in roads:
        print(f"  {a} - {b} ({w} km)")
    print(f"  Total road length: {total} km")

    print("\n4. ROAD CLOSED between College and Hospital!")
    city.close_road("College", "Hospital")
    path, km = city.shortest_route(start, goal)
    show_route(f"   New shortest route ({start} to {goal})", path, km)

    print("\n--- Try your own route ---")
    print("Places:", ", ".join(city.roads))
    while True:
        a = input("\nStart (or press Enter to quit): ").strip()
        if not a:
            break
        b = input("Destination: ").strip()
        if a not in city.roads or b not in city.roads:
            print("Unknown place, check the spelling.")
            continue
        path, km = city.shortest_route(a, b)
        show_route("Shortest route", path, km)
if __name__ == "__main__":
    main()