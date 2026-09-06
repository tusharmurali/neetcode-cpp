# 1396. Design Underground System

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/design-underground-system/>  
- **NeetCode:** <https://neetcode.io/problems/design-underground-system>  
- **Video:** <https://www.youtube.com/watch?v=W5QOLqXskZM>  

[← Back to index](../INDEX.md)

## 1. Two HashMaps

We need to track passenger trips and compute average travel times between stations. Each passenger checks in at one station and checks out at another, forming a route. By storing check-in information and aggregating travel times for each route, we can efficiently calculate averages without storing individual trip details.

```cpp
class UndergroundSystem {
    unordered_map<int, pair<string, int>> checkInMap;
    unordered_map<string, pair<int, int>> routeMap;

public:
    UndergroundSystem() {}

    void checkIn(int id, string startStation, int t) {
        checkInMap[id] = {startStation, t};
    }

    void checkOut(int id, string endStation, int t) {
        auto [startStation, time] = checkInMap[id];
        string route = startStation + "," + endStation;
        if (!routeMap.count(route))
            routeMap[route] = {0, 0};
        routeMap[route].first += t - time;
        routeMap[route].second += 1;
    }

    double getAverageTime(string startStation, string endStation) {
        string route = startStation + "," + endStation;
        auto [totalTime, count] = routeMap[route];
        return (double) totalTime / count;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(1)$ time for each $checkIn()$ function call.
    - $O(m)$ time for each $checkOut()$ and $getAverageTime()$ function calls.
- Space complexity: $O(n + N ^ 2)$

> Where $n$ is the number of passengers, $N$ is the total number of stations, and $m$ is the average length of station name.

## 2. Two HashMaps + Hashing

The previous approach uses string concatenation to create route keys, which can be slow for long station names. By computing a hash value for each route instead of concatenating strings, we can achieve faster lookups. Using double hashing (two different hash functions) reduces collision probability while maintaining `O(1)` average lookup time.

```cpp
class UndergroundSystem {
private:
    static constexpr int MOD1 = 768258391, MOD2 = 685683731;
    static constexpr int BASE1 = 37, BASE2 = 31;
    unordered_map<int, pair<string, int>> checkInMap;
    unordered_map<unsigned long long, pair<int, int>> routeMap;

    unsigned long long getHash(const string& s1, const string& s2) {
        long long h1 = 0, h2 = 0, p1 = 1, p2 = 1;
        string combined = s1 + "," + s2;

        for (char c : combined) {
            h1 = (h1 + (c - 96) * p1) % MOD1;
            h2 = (h2 + (c - 96) * p2) % MOD2;
            p1 = (p1 * BASE1) % MOD1;
            p2 = (p2 * BASE2) % MOD2;
        }
        return (h1 << 32) | h2;
    }

public:
    UndergroundSystem() {}

    void checkIn(int id, string startStation, int t) {
        checkInMap[id] = {startStation, t};
    }

    void checkOut(int id, string endStation, int t) {
        auto [startStation, time] = checkInMap[id];
        unsigned long long routeHash = getHash(startStation, endStation);
        routeMap[routeHash].first += (t - time);
        routeMap[routeHash].second++;
    }

    double getAverageTime(string startStation, string endStation) {
        unsigned long long routeHash = getHash(startStation, endStation);
        auto [totalTime, count] = routeMap[routeHash];
        return (double) totalTime / count;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(1)$ time for each $checkIn()$ function call.
    - $O(m)$ time for each $checkOut()$ and $getAverageTime()$ function calls.
- Space complexity: $O(n + N ^ 2)$

> Where $n$ is the number of passengers, $N$ is the total number of stations, and $m$ is the average length of station name.
