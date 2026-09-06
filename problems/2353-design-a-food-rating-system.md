# 2353. Design a Food Rating System

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/design-a-food-rating-system/>  
- **NeetCode:** <https://neetcode.io/problems/design-a-food-rating-system>  
- **Video:** <https://www.youtube.com/watch?v=Ikp8SgbgbEo>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest approach stores each food's rating in a hash map and groups foods by their cuisine in another hash map. When we need the highest-rated food for a cuisine, we scan through all foods in that cuisine and find the maximum. This is straightforward but inefficient for frequent queries since we examine every food each time.

```cpp
class FoodRatings {
private:
    unordered_map<string, int> foodToRating;
    unordered_map<string, vector<string>> cuisineToFood;

public:
    FoodRatings(vector<string>& foods, vector<string>& cuisines, vector<int>& ratings) {
        for (size_t i = 0; i < foods.size(); i++) {
            foodToRating[foods[i]] = ratings[i];
            cuisineToFood[cuisines[i]].push_back(foods[i]);
        }
    }

    void changeRating(string food, int newRating) {
        foodToRating[food] = newRating;
    }

    string highestRated(string cuisine) {
        int maxR = 0;
        string res = "";
        for (const string& food : cuisineToFood[cuisine]) {
            int r = foodToRating[food];
            if (r > maxR || (r == maxR && food < res)) {
                res = food;
                maxR = r;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity:
    - $O(n)$ time for initialization.
    - $O(1)$ time for each $changeRating()$ function call.
    - $O(n)$ time for each $highestRated()$ function call.
- Space complexity: $O(n)$

## 2. Heap

Using a max-heap (priority queue) for each cuisine allows us to quickly access the highest-rated food. The challenge is handling rating updates: removing an element from the middle of a heap is expensive. Instead, we use lazy deletion. When a rating changes, we push a new entry with the updated rating. When querying, we check if the top entry's rating matches the current rating in our hash map. If not, it is stale, and we pop it until we find a valid entry.

```cpp
class FoodRatings {
    unordered_map<string, int> foodToRating;
    unordered_map<string, string> foodToCuisine;
    struct cmp {
        bool operator()(const pair<int, string>& a, const pair<int, string>& b) {
            if (a.first == b.first) return a.second > b.second;
            return a.first < b.first;
        }
    };
    unordered_map<string, priority_queue<pair<int, string>,
                    vector<pair<int, string>>, cmp>> cuisineToHeap;

public:
    FoodRatings(vector<string>& foods, vector<string>& cuisines, vector<int>& ratings) {
        for (int i = 0; i < foods.size(); i++) {
            foodToRating[foods[i]] = ratings[i];
            foodToCuisine[foods[i]] = cuisines[i];
            cuisineToHeap[cuisines[i]].push({ratings[i], foods[i]});
        }
    }

    void changeRating(string food, int newRating) {
        string cuisine = foodToCuisine[food];
        foodToRating[food] = newRating;
        cuisineToHeap[cuisine].push({newRating, food});
    }

    string highestRated(string cuisine) {
        auto &heap = cuisineToHeap[cuisine];
        while (!heap.empty()) {
            auto [rating, food] = heap.top();
            if (foodToRating[food] == rating) return food;
            heap.pop();
        }
        return "";
    }
};
```

**Complexity**

- Time complexity:
    - $O(n \log n)$ time for initialization.
    - $O(\log n)$ time for each $changeRating()$ function call.
    - $O(\log n)$ time for each $highestRated()$ function call.
- Space complexity: $O(n)$

## 3. Sorted Set

A sorted set (like `TreeSet` or `SortedSet`) maintains elements in sorted order and supports efficient insertion, deletion, and access to the minimum/maximum element. For each cuisine, we store `(negative rating, food name)` pairs so the smallest element corresponds to the highest rating. When updating a rating, we remove the old entry and insert the new one. Querying simply returns the first element of the set.

```cpp
class FoodRatings {
    unordered_map<string, int> foodToRating;
    unordered_map<string, string> foodToCuisine;
    unordered_map<string, set<pair<int, string>>> cuisineToSet;

public:
    FoodRatings(vector<string>& foods, vector<string>& cuisines, vector<int>& ratings) {
        for (int i = 0; i < foods.size(); i++) {
            foodToRating[foods[i]] = ratings[i];
            foodToCuisine[foods[i]] = cuisines[i];
            cuisineToSet[cuisines[i]].insert({-ratings[i], foods[i]});
        }
    }

    void changeRating(string food, int newRating) {
        string cuisine = foodToCuisine[food];
        auto& s = cuisineToSet[cuisine];

        s.erase({-foodToRating[food], food});
        foodToRating[food] = newRating;
        s.insert({-newRating, food});
    }

    string highestRated(string cuisine) {
        return begin(cuisineToSet[cuisine])->second;
    }
};
```

**Complexity**

- Time complexity:
    - $O(n \log n)$ time for initialization.
    - $O(\log n)$ time for each $changeRating()$ function call.
    - $O(1)$ in Python and $O(\log n)$ in other languages for each $highestRated()$ function call.
- Space complexity: $O(n)$
