# 1243. Array Transformation

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/array-transformation/>  
- **NeetCode:** <https://neetcode.io/problems/array-transformation>  

[← Back to index](../INDEX.md)

## 1. Simulation (Extra Space)

```cpp
class Solution {
public:
    vector<int> transformArray(vector<int>& arr) {
        bool changed = true;
        while (changed) {
            changed = false;
            vector<int> prev = arr;
            for (int i = 1; i < (int)arr.size() - 1; i++) {
                if (prev[i] > prev[i - 1] && prev[i] > prev[i + 1]) {
                    arr[i]--;
                    changed = true;
                } else if (prev[i] < prev[i - 1] && prev[i] < prev[i + 1]) {
                    arr[i]++;
                    changed = true;
                }
            }
        }
        return arr;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot (n + m))$
- Space complexity: $O(n)$

> Where $n$ is the length of the array $arr$ and $m$ is the maximum value in $arr$.

## 2. Simulation

```cpp
class Solution {
public:
    vector<int> transformArray(vector<int>& arr) {
        bool changed = true;
        while (changed) {
            changed = false;
            int prev = arr[0];
            for (int i = 1; i < (int)arr.size() - 1; i++) {
                int cur = arr[i];
                if (cur > prev && cur > arr[i + 1]) {
                    arr[i]--;
                    changed = true;
                } else if (cur < prev && cur < arr[i + 1]) {
                    arr[i]++;
                    changed = true;
                }
                prev = cur;
            }
        }
        return arr;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot (n + m))$
- Space complexity: $O(1)$ extra space.

> Where $n$ is the length of the array $arr$ and $m$ is the maximum value in $arr$.

## 3. Simulation (Optimal)

```cpp
class Solution {
public:
    vector<int> transformArray(vector<int>& arr) {
        int n = arr.size();
        bool changed = true;
        while (changed) {
            changed = false;
            int i = 1;
            while (i < n - 1) {
                if (!isExtremum(arr, i)) {
                    i++;
                    continue;
                }

                int j = i;
                while (j < n - 1 && isExtremum(arr, j)) {
                    j++;
                }

                int steps = INT_MAX;
                for (int k = i; k < j; k++) {
                    int left = abs(arr[k] - arr[k - 1]);
                    int right = abs(arr[k] - arr[k + 1]);
                    if (k > i) {
                        left = (left + 1) / 2;
                    }
                    if (k < j - 1) {
                        right = (right + 1) / 2;
                    }
                    steps = min(steps, min(left, right));
                }

                for (int k = i; k < j; k++) {
                    if (arr[k] < arr[k + 1]) {
                        arr[k] += steps;
                    } else {
                        arr[k] -= steps;
                    }
                }

                changed = true;
                i = j;
            }
        }
        return arr;
    }

private:
    bool isExtremum(vector<int>& arr, int i) {
        return (arr[i] > arr[i - 1] && arr[i] > arr[i + 1]) ||
               (arr[i] < arr[i - 1] && arr[i] < arr[i + 1]);
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot (n + m))$
- Space complexity: $O(1)$ extra space.

> Where $n$ is the length of the array $arr$ and $m$ is the maximum value in $arr$.
