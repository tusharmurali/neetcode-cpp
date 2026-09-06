# 1133. Largest Unique Number

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/largest-unique-number/>  
- **NeetCode:** <https://neetcode.io/problems/largest-unique-number>  

[← Back to index](../INDEX.md)

## 1. Sorting

After sorting in descending order, we can scan from largest to smallest. A number is unique if it differs from its neighbors. We skip over groups of duplicates and return the first number that appears exactly once.

```cpp
class Solution {
public:
    int largestUniqueNumber(vector<int>& nums) {
        int n = nums.size();

        // If there's only one element, it's unique by default
        if (n == 1) {
            return nums[0];
        }

        sort(nums.begin(), nums.end(), greater<int>());

        // Start from the beginning (largest numbers)
        int currentIndex = 0;

        while (currentIndex < n) {
            // If it's the last element or different from the next one,
            // it's unique
            if (currentIndex == n - 1 ||
                nums[currentIndex] != nums[currentIndex + 1]) {
                return nums[currentIndex];
            }

            // Skip duplicates
            while (currentIndex < n - 1 &&
                   nums[currentIndex] == nums[currentIndex + 1]) {
                currentIndex++;
            }

            // Move to the next unique number
            currentIndex++;
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot \log n)$
- Space complexity: $O(S)$ Depends on the language of implementation

> Where $n$ is the length of the `nums` array and $S$ is the sorting algorthm

## 2. Sorted Map

We can count the frequency of each number using a sorted map (tree map). Since the map maintains keys in sorted order, we iterate from the largest key downward and return the first key with frequency `1`.

```cpp
class Solution {
public:
    int largestUniqueNumber(vector<int>& nums) {
        // Use a map to store numbers and their frequencies
        map<int, int> frequencyMap;

        // Populate the frequencyMap
        for (int num : nums) {
            frequencyMap[num]++;
        }

        // Initialize the result to -1 (default if no unique number is found)
        int largestUnique = -1;

        // Iterate through the map in reverse order (largest to smallest)
        for (auto it = frequencyMap.rbegin(); it != frequencyMap.rend(); ++it) {
            // If the frequency is 1, we've found our largest unique number
            if (it->second == 1) {
                largestUnique = it->first;
                break;
            }
        }

        return largestUnique;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot \log n)$
- Space complexity: $O(n)$

> Where $n$ is the length of the `nums` array.

## 3. Map

Using a regular hash map, we count frequencies in linear time. Then we scan all entries and track the maximum number with frequency `1`. This avoids the overhead of maintaining sorted order.

```cpp
class Solution {
public:
    int largestUniqueNumber(vector<int>& nums) {
        // Create an unordered_map to store the frequency of each number
        unordered_map<int, int> frequencyMap;

        // Populate the frequencyMap
        for (int num : nums) {
            frequencyMap[num]++;
        }

        // Initialize the result to -1 (default if no unique number is found)
        int largestUnique = -1;

        for (auto& pair : frequencyMap) {
            // Check if the number appears only once and is larger than the
            // current largestUnique
            if (pair.second == 1 && pair.first > largestUnique) {
                largestUnique = pair.first;
            }
        }

        return largestUnique;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the length of the `nums` array.
