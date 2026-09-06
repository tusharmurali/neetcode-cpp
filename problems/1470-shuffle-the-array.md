# 1470. Shuffle the Array

- **Difficulty:** Easy  
- **Pattern:** Bit Manipulation  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/shuffle-the-array/>  
- **NeetCode:** <https://neetcode.io/problems/shuffle-the-array>  
- **Video:** <https://www.youtube.com/watch?v=IvIKD_EU8BY>  

[← Back to index](../INDEX.md)

## 1. Iteration (Extra Space)

The array is given as `[x1, x2, ..., xn, y1, y2, ..., yn]` and we need to rearrange it to `[x1, y1, x2, y2, ..., xn, yn]`. The simplest approach is to iterate through the first half of the array and alternate between picking elements from the first half (`x` values at index `i`) and the second half (`y` values at index `i + n`). We build the result in a new array.

```cpp
class Solution {
public:
    vector<int> shuffle(vector<int>& nums, int n) {
        vector<int> res;
        for (int i = 0; i < n; i++) {
            res.push_back(nums[i]);
            res.push_back(nums[i + n]);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ extra space.

## 2. Multiplication And Modulo

To shuffle in-place without extra space, we can encode two values in a single array element. Since values are at most 1000, we pick a base `M > 1000`. For each position `i` in the result, we determine which original element belongs there and encode it by adding `original_value * M` to `nums[i]`. The original value is retrieved using `nums[index] % M` (since we have not yet divided), and the new value is stored in the upper part. After encoding all positions, we divide each element by `M` to extract the shuffled values.

```cpp
class Solution {
public:
    vector<int> shuffle(vector<int>& nums, int n) {
        int M = *max_element(nums.begin(), nums.end()) + 1;
        for (int i = 0; i < 2 * n; i++) {
            if (i % 2 == 0) {
                nums[i] += (nums[i / 2] % M) * M;
            } else {
                nums[i] += (nums[n + i / 2] % M) * M;
            }
        }
        for (int i = 0; i < 2 * n; i++) {
            nums[i] /= M;
        }
        return nums;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 3. Bit Manipulation

Similar to the multiplication approach, we can use bit manipulation to pack two values into one integer. Since values fit in 10 bits (max 1000 < 1024 = 2^10), we can store one value in the lower 10 bits and another in the upper bits. First, we pack each `x` and its corresponding `y` into the first half of the array. Then we unpack them from back to front into their final interleaved positions, ensuring we do not overwrite values we still need.

```cpp
class Solution {
public:
    vector<int> shuffle(vector<int>& nums, int n) {
        for (int i = 0; i < n; i++) {
            nums[i] = (nums[i] << 10) | nums[i + n]; // Store x, y in nums[i]
        }

        int j = 2 * n - 1;
        for (int i = n - 1; i >= 0; i--) {
            int y = nums[i] & ((1 << 10) - 1);
            int x = nums[i] >> 10;
            nums[j] = y;
            nums[j - 1] = x;
            j -= 2;
        }

        return nums;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/1470-shuffle-the-array.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
	vector<int> shuffle(vector<int>& nums, int n) {
		int lp = 0;
		int rp = n;
		int p = 0;
		vector<int> shuffled(2*n);
		
		while (p < 2 * n) {
			shuffled[p++] = nums[lp++];
			shuffled[p++] = nums[rp++];
		}
		return shuffled;
	}
};
```
