# 2013. Detect Squares

- **Difficulty:** Medium  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/detect-squares/>  
- **NeetCode:** <https://neetcode.io/problems/count-squares>  
- **Video:** <https://www.youtube.com/watch?v=bahebearrDc>  
- **Video approach:** 1. Hash Map - I  

[← Back to index](../INDEX.md)

## 1. Hash Map - I ▶ video

We are asked to count how many **axis-aligned squares** can be formed using a given point as one corner and previously added points as the other three corners.

Key observations about an axis-aligned square:

- All sides are parallel to the x-axis and y-axis
- If `(px, py)` is one corner and `(x, y)` is the **diagonal opposite corner**, then:
    - `|px - x| == |py - y|` (equal side lengths)
    - `x != px` and `y != py` (otherwise it would not form a square)
- The other two required corners must be:
    - `(x, py)`
    - `(px, y)`

So the idea is:

- Fix the query point `(px, py)`
- Try every previously added point `(x, y)` as a **possible diagonal**
- If it forms a valid square diagonal, multiply how many times the other two required points exist

A hash map lets us quickly check how many times a specific point was added.

```cpp
class CountSquares {
private:
    unordered_map<long, int> ptsCount;
    vector<vector<int>> pts;

    long getKey(int x, int y) {
        return (static_cast<long>(x) << 32) | static_cast<long>(y);
    }

public:
    CountSquares() {
    }

    void add(vector<int> point) {
        long key = getKey(point[0], point[1]);
        ptsCount[key]++;
        pts.push_back(point);
    }

    int count(vector<int> point) {
        int res = 0;
        int px = point[0], py = point[1];

        for (const auto& pt : pts) {
            int x = pt[0], y = pt[1];
            if (abs(py - y) != abs(px - x) || x == px || y == py) continue;
            res += ptsCount[getKey(x, py)] * ptsCount[getKey(px, y)];
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(1)$ for $add()$, $O(n)$ for $count()$.
- Space complexity: $O(n)$

## 2. Hash Map - II

We want to count how many **axis-aligned squares** can be formed using the given query point `(x1, y1)` as one corner.

For an axis-aligned square:

- One side is vertical and one side is horizontal
- If we pick another point `(x1, y2)` on the **same vertical line** (same `x1`), then:
    - the side length is `side = y2 - y1`
    - this determines where the square’s other x-coordinates must be:
        - `x3 = x1 + side` (square to the right)
        - `x4 = x1 - side` (square to the left)

So for each possible vertical partner `(x1, y2)`, we can form up to **two squares**:

1. Square to the **right** needs points:
    - `(x3, y1)` and `(x3, y2)`
2. Square to the **left** needs points:
    - `(x4, y1)` and `(x4, y2)`

Because points can be added multiple times, the total number of squares is the product of the counts of the required points.

This version uses a nested hash map:

- `ptsCount[x][y]` = how many times point `(x, y)` was added
  which makes counting fast and avoids storing a list of all points.

```cpp
class CountSquares {
    unordered_map<int, unordered_map<int, int>> ptsCount;

public:
    CountSquares() {}

    void add(vector<int> point) {
        ptsCount[point[0]][point[1]]++;
    }

    int count(vector<int> point) {
        int res = 0;
        int x1 = point[0], y1 = point[1];

        for (auto &[y2, cnt] : ptsCount[x1]) {
            int side = y2 - y1;
            if (side == 0) continue;

            int x3 = x1 + side, x4 = x1 - side;
            res += cnt * ptsCount[x3][y1] * ptsCount[x3][y2];
            res += cnt * ptsCount[x4][y1] * ptsCount[x4][y2];
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(1)$ for $add()$, $O(n)$ for $count()$.
- Space complexity: $O(n)$

## Standalone solution file (`cpp/2013-detect-squares.cpp` in the NeetCode repo)

```cpp
/*
    Given stream of points, add new points, return count of squares

    Find diagonals, if exists then forms a square, loop thru all points

    Time: O(1) add O(n^2) count -> n = number of points
    Space: O(n)
*/

class DetectSquares {
public:
    DetectSquares() {
        
    }
    
    void add(vector<int> point) {
        points[point[0]][point[1]]++;
    }
    
    int count(vector<int> point) {
        int x1 = point[0];
        int y1 = point[1];
        
        int result = 0;
        
        for (auto x = points.begin(); x != points.end(); x++) {
            unordered_map<int, int> yPoints = x->second;
            for (auto y = yPoints.begin(); y != yPoints.end(); y++) {
                int x3 = x->first;
                int y3 = y->first;
                
                // skip points on same x-axis or y-axis
                if (abs(x3 - x1) == 0 || abs(x3 - x1) != abs(y3 - y1)) {
                    continue;
                }
                
                result += points[x3][y3] * points[x1][y3] * points[x3][y1];
            }
        }
        
        return result;
    }
private:
    // {x -> {y -> count}}
    unordered_map<int, unordered_map<int, int>> points;
};

/**
 * Your DetectSquares object will be instantiated and called as such:
 * DetectSquares* obj = new DetectSquares();
 * obj->add(point);
 * int param_2 = obj->count(point);
 */
```
