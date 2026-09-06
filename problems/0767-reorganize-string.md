# 767. Reorganize String

- **Difficulty:** Medium  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/reorganize-string/>  
- **NeetCode:** <https://neetcode.io/problems/reorganize-string>  
- **Video:** <https://www.youtube.com/watch?v=2g_b1aYTHeg>  
- **Video approach:** 2. Frequency Count (Max-Heap)  

[← Back to index](../INDEX.md)

## 1. Frequency Count

To avoid adjacent duplicates, we should always place the most frequent remaining character, then the second most frequent. This greedy approach works because alternating between the two most common characters maximizes our ability to separate identical characters. If any character appears more than `(n + 1) / 2`, reorganization is impossible.

```cpp
class Solution {
public:
    string reorganizeString(string s) {
        vector<int> freq(26, 0);
        for (char c : s) {
            freq[c - 'a']++;
        }

        int maxFreq = *max_element(freq.begin(), freq.end());
        if (maxFreq > (s.size() + 1) / 2) {
            return "";
        }

        string res;
        while (res.size() < s.size()) {
            int maxIdx = findMaxIndex(freq);
            char maxChar = 'a' + maxIdx;
            res += maxChar;
            freq[maxIdx]--;

            if (freq[maxIdx] == 0) {
                continue;
            }

            int tmp = freq[maxIdx];
            freq[maxIdx] = INT_MIN;
            int nextMaxIdx = findMaxIndex(freq);
            char nextMaxChar = 'a' + nextMaxIdx;
            res += nextMaxChar;
            freq[maxIdx] = tmp;
            freq[nextMaxIdx]--;
        }

        return res;
    }

private:
    int findMaxIndex(const vector<int>& freq) {
        int maxIdx = 0;
        for (int i = 1; i < freq.size(); i++) {
            if (freq[i] > freq[maxIdx]) {
                maxIdx = i;
            }
        }
        return maxIdx;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space, since we have at most $26$ different characters.
    - $O(n)$ space for the output string.

## 2. Frequency Count (Max-Heap) ▶ video

A `maxHeap` efficiently gives us the most frequent character at any time. We pop the top character, add it to `res`, then push it back with decremented count after processing the next character. This delay ensures we never place the same character twice in a row. If the heap is empty but we still have a `prev` pending character, reorganization failed.

```cpp
class Solution {
public:
    string reorganizeString(string s) {
        vector<int> freq(26, 0);
        for (char& c : s) {
            freq[c - 'a']++;
        }

        priority_queue<pair<int, char>> maxHeap;
        for (int i = 0; i < 26; i++) {
            if (freq[i] > 0) {
                maxHeap.push({freq[i], 'a' + i});
            }
        }

        string res = "";
        pair<int, char> prev = {0, ' '};
        while (!maxHeap.empty() || prev.first > 0) {
            if (prev.first > 0 && maxHeap.empty()) {
                return "";
            }

            auto [count, char_] = maxHeap.top();
            maxHeap.pop();
            res += char_;
            count--;

            if (prev.first > 0) {
                maxHeap.push(prev);
            }

            prev = {count, char_};
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space, since we have at most $26$ different characters.
    - $O(n)$ space for the output string.

## 3. Frequency Count (Greedy)

Instead of building the string character by character, we can place characters at alternating indices. First, fill all even indices (0, 2, 4, ...) with the most frequent character. This guarantees no two identical characters are adjacent since they are separated by at least one position. Then fill the remaining positions with other characters, wrapping to odd indices when even slots are exhausted. We use `idx` to track the current position and update it using `idx += 2`.

```cpp
class Solution {
public:
    string reorganizeString(string s) {
        vector<int> freq(26, 0);
        for (char& c : s) {
            freq[c - 'a']++;
        }

        int maxIdx = max_element(freq.begin(), freq.end()) - freq.begin();
        int maxFreq = freq[maxIdx];
        if (maxFreq > (s.size() + 1) / 2) {
            return "";
        }

        string res(s.size(), ' ');
        int idx = 0;
        char maxChar = 'a' + maxIdx;

        while (freq[maxIdx] > 0) {
            res[idx] = maxChar;
            idx += 2;
            freq[maxIdx]--;
        }

        for (int i = 0; i < 26; i++) {
            while (freq[i] > 0) {
                if (idx >= s.size()) {
                    idx = 1;
                }
                res[idx] = 'a' + i;
                idx += 2;
                freq[i]--;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space, since we have at most $26$ different characters.
    - $O(n)$ space for the output string.

## Standalone solution file (`cpp/0767-reorganize-string.cpp` in the NeetCode repo)

```cpp
// Time: O(NlogN)
// Space: O(N)

class Solution {
public:
    string reorganizeString(string s) {
        string res="";

        unordered_map<char, int> mp;
        priority_queue<pair<int, char>> maxh;
        
        for(auto ch : s)
            mp[ch] += 1;
        
        for(auto m : mp)
            maxh.push(make_pair(m.second, m.first));
        
        while(maxh.size() > 1){
            auto top1= maxh.top();
            maxh.pop();
            auto top2 = maxh.top();
            maxh.pop();
            
            res += top1.second;
            res += top2.second;
            
            if(--top1.first > 0)
                maxh.push(top1);
            
            if(--top2.first > 0)
                maxh.push(top2);
        }
        
        if(!maxh.empty()){
            if(maxh.top().first > 1)
                return "";
            
            else
                res += maxh.top().second;
        }
        
        return res;
    }
};
```
