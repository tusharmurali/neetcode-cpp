# 1231. Divide Chocolate

- **Difficulty:** Hard  
- **Pattern:** Binary Search  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/divide-chocolate/>  
- **NeetCode:** <https://neetcode.io/problems/divide-chocolate>  

[← Back to index](../INDEX.md)

## 1. Binary Search + Greedy

We want to maximize the minimum sweetness we receive after dividing the chocolate bar into `k + 1` pieces. This is a classic binary search on the answer pattern. We binary search on possible sweetness values: for each candidate value `mid`, we greedily check if we can divide the bar so that at least `k + 1` people each get a piece with sweetness at least `mid`. If we can, we try a higher value; if not, we try a lower one.

```cpp
class Solution {
public:
    int maximizeSweetness(vector<int>& sweetness, int k) {
        // Initialize the left and right boundaries.
        // left = 1 and right = total sweetness / number of people.
        int numberOfPeople = k + 1;
        int left = *min_element(sweetness.begin(), sweetness.end());
        int right = accumulate(sweetness.begin(), sweetness.end(), 0) / numberOfPeople;

        while (left < right) {
            // Get the middle index between left and right boundary indexes.
            // cur_sweetness stands for the total sweetness for the current person.
            // people_with_chocolate stands for the number of people that have
            // a piece of chocolate of sweetness greater than or equal to mid.
            int mid = (left + right + 1) / 2;
            int curSweetness = 0;
            int peopleWithChocolate = 0;

            // Start assigning chunks to the current people,.
            for (int s : sweetness) {
                curSweetness += s;

                // When the total sweetness from him is no less than mid, meaning we
                // have done with him and move on to assigning chunks to the next people.
                if (curSweetness >= mid) {
                    peopleWithChocolate += 1;
                    curSweetness = 0;
                }
            }

            // Check if we successfully give everyone a piece of chocolate with sweetness
            // no less than mid, and eliminate the search space by half.
            if (peopleWithChocolate >= numberOfPeople) {
                left = mid;
            } else {
                right = mid - 1;
            }
        }

        // Once the left and right boundaries coincide, we find the target value,
        // that is, the maximum possible sweetness we can get.
        return right;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot \log(S/(k + 1)))$
    - The lower and upper bounds are `min(sweetness)` and `S / (k + 1)` respectively. In the worst case (when `k` is small), the right boundary will have the same magnitude as `S`, and the left boundary will be `1`. Thus, the maximum possible time complexity for a single binary search is $O(\log S)$.
      For every single search, we need to traverse the chocolate bar in order to allocate chocolate chunks to everyone, which takes $O(n)$ time.

- Space complexity: $O(1)$ constant space

> Where $n$ is the number of chunks in the chocolate, and $S$ is the total sweetness of the chocolate bar.
