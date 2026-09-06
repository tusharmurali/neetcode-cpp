# 149. Maximum Points on a Line

- **Difficulty:** Hard  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/max-points-on-a-line/>  
- **NeetCode:** <https://neetcode.io/problems/max-points-on-a-line>  
- **Video:** <https://www.youtube.com/watch?v=Bb9lOXUOnFw>  
- **Video approach:** 2. Math + Hash Map (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Math

Points are collinear if they share the same slope when measured from a common reference point. For each pair of points, we compute the slope and then check how many other points lie on that same line. By fixing two points and iterating through all remaining points to count matches, we can find the maximum number of collinear points. This triple nested loop is simple but has cubic time complexity.

```cpp
class Solution {
public:
    int maxPoints(vector<vector<int>>& points) {
        int n = points.size();
        if (n <= 2) {
            return n;
        }

        int res = 1;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                double slope = getSlope(points[i], points[j]);
                int cnt = 2;
                for (int k = j + 1; k < n; k++) {
                    if (slope == getSlope(points[i], points[k])) {
                        cnt++;
                    }
                }
                res = max(res, cnt);
            }
        }

        return res;
    }

private:
    double getSlope(vector<int>& p1, vector<int>& p2) {
        if (p1[0] == p2[0]) {
            return INFINITY;
        }
        return (double)(p2[1] - p1[1]) / (p2[0] - p1[0]);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(1)$ extra space.

## 2. Math + Hash Map ▶ video

Instead of checking every pair and then scanning all other points, we can fix one point and use a hash map to group all other points by their slope relative to the fixed point. Points with the same slope lie on the same line through the fixed point. The largest group size plus one (for the fixed point itself) gives the maximum collinear points for that reference. Repeating this for every point as the reference yields the global maximum.

```cpp
class Solution {
public:
    int maxPoints(vector<vector<int>>& points) {
        int res = 1;
        for (int i = 0; i < points.size(); i++) {
            vector<int>& p1 = points[i];
            unordered_map<double, int> count;
            for (int j = i + 1; j < points.size(); j++) {
                vector<int>& p2 = points[j];
                double slope = (p2[0] == p1[0]) ? INFINITY :
                               (double)(p2[1] - p1[1]) / (p2[0] - p1[0]);
                count[slope]++;
                res = max(res, count[slope] + 1);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 3. Math + Hash Map (Optimal)

Floating point slopes can introduce precision errors. To avoid this, we represent the slope as a reduced fraction using the GCD of the differences in x and y coordinates. By storing slopes as pairs (or strings) of integers rather than floating point numbers, we eliminate rounding issues. This approach maintains the same algorithmic structure as the previous solution but with more robust comparisons.

```cpp
class Solution {
public:
    int maxPoints(vector<vector<int>>& points) {
        if (points.size() <= 2) {
            return points.size();
        }

        int res = 1;
        for (int i = 0; i < points.size() - 1; i++) {
            unordered_map<string, int> count;
            for (int j = i + 1; j < points.size(); j++) {
                int dx = points[j][0] - points[i][0];
                int dy = points[j][1] - points[i][1];
                int g = gcd(dx, dy);
                dx /= g;
                dy /= g;
                string slope = to_string(dx) + ":" + to_string(dy);
                count[slope]++;
            }
            for (const auto& [slope, freq] : count) {
                res = max(res, freq + 1);
            }
        }
        return res;
    }

private:
    int gcd(int a, int b) {
        return b == 0 ? a : gcd(b, a % b);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 \log m)$
- Space complexity: $O(n)$

> Where $n$ is the number of points and $m$ is the maximum value in the points.

## Standalone solution file (`cpp/0149-max-points-on-a-line.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int maxPoints(vector<vector<int>>& points) {
        int res = 1;
        for (int i=0; i<points.size(); ++i) {
            unordered_map<float, int> count;
            for (int j=i+1; j<points.size(); ++j) {
                float s = slope(points[i], points[j]);
                count[s] ++; 
                res = max(res, count[s] + 1);
            }
        }
        return res;
    }
private:
    float slope(vector<int>& p1, vector<int>& p2) {
        if ((p2[0] - p1[0]) == 0) 
            return INT_MAX; // aka edge case to handle a slope of infinity
        return (float) (p2[1] - p1[1]) / (float) (p2[0] - p1[0]);
    }
};
```
