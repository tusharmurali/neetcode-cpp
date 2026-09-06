# 229. Majority Element II

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/majority-element-ii/>  
- **NeetCode:** <https://neetcode.io/problems/majority-element-ii>  
- **Video:** <https://www.youtube.com/watch?v=Eua-UrQ_ANo>  

[← Back to index](../INDEX.md)

## 1. Brute Force

Elements appearing more than `n/3` times are rare. There can be at most two such elements. For each unique element, we count its occurrences and check if it exceeds `n/3`. We use a set to avoid adding duplicates to the result.

```cpp
class Solution {
public:
    vector<int> majorityElement(vector<int>& nums) {
        unordered_set<int> res;
        for (int num : nums) {
            int count = 0;
            for (int i : nums) {
                if (i == num) count++;
            }
            if (count > nums.size() / 3) {
                res.insert(num);
            }
        }
        return vector<int>(res.begin(), res.end());
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ since output array size will be at most $2$.

## 2. Sorting

After sorting, identical elements are grouped together. We can scan through and count consecutive runs of each element. If a run's length exceeds `n/3`, we add that element to our result. This approach avoids the nested loops of brute force.

```cpp
class Solution {
public:
    vector<int> majorityElement(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<int> res;
        int n = nums.size();

        int i = 0;
        while (i < n) {
            int j = i + 1;
            while (j < n && nums[i] == nums[j]) {
                j++;
            }
            if (j - i > n / 3) {
                res.push_back(nums[i]);
            }
            i = j;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 3. Frequency Count

We can count each element's frequency in a single pass using a hash map. Then we iterate through the map and collect all elements whose count exceeds `n/3`. This trades space for time compared to the brute force approach.

```cpp
class Solution {
public:
    vector<int> majorityElement(vector<int>& nums) {
        unordered_map<int, int> count;
        for (int num : nums) {
            count[num]++;
        }

        vector<int> res;
        for (auto& pair : count) {
            if (pair.second > nums.size() / 3) {
                res.push_back(pair.first);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Boyer-Moore Voting Algorithm

The Boyer-Moore algorithm extends to finding up to two majority elements. We maintain two candidates with their counts. When we see a candidate, we increment its count. When we see a different element and both counts are positive, we decrement both. When a count is `0`, we replace that candidate. After one pass, we verify the candidates by counting their actual occurrences.

```cpp
class Solution {
public:
    vector<int> majorityElement(vector<int>& nums) {
        int n = nums.size();
        int num1 = -1, num2 = -1, cnt1 = 0, cnt2 = 0;

        for (int num : nums) {
            if (num == num1) {
                cnt1++;
            } else if (num == num2) {
                cnt2++;
            } else if (cnt1 == 0) {
                num1 = num;
                cnt1 = 1;
            } else if (cnt2 == 0) {
                num2 = num;
                cnt2 = 1;
            } else {
                cnt1--;
                cnt2--;
            }
        }

        cnt1 = cnt2 = 0;
        for (int num : nums) {
            if (num == num1) cnt1++;
            else if (num == num2) cnt2++;
        }

        vector<int> res;
        if (cnt1 > n / 3) res.push_back(num1);
        if (cnt2 > n / 3) res.push_back(num2);

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since output array size will be at most $2$.

## 5. Boyer-Moore Voting Algorithm (Hash Map)

This variation uses a hash map to track candidates instead of fixed variables. We allow at most 2 elements in the map. When a third element tries to enter, we decrement all counts and remove elements with count `0`. This generalizes the Boyer-Moore approach and can be extended to find elements appearing more than `n/k` times.

```cpp
class Solution {
public:
    vector<int> majorityElement(vector<int>& nums) {
        unordered_map<int, int> count;

        for (int num : nums) {
            count[num]++;

            if (count.size() > 2) {
                unordered_map<int, int> newCount;
                for (auto& entry : count) {
                    if (entry.second > 1) {
                        newCount[entry.first] = entry.second - 1;
                    }
                }
                count = newCount;
            }
        }

        vector<int> res;
        for (auto& entry : count) {
            int frequency = 0;
            for (int num : nums) {
                if (num == entry.first) frequency++;
            }
            if (frequency > nums.size() / 3) {
                res.push_back(entry.first);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since output array size will be at most $2$.
