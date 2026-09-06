# 358. Rearrange String k Distance Apart

- **Difficulty:** Hard  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/rearrange-string-k-distance-apart/>  
- **NeetCode:** <https://neetcode.io/problems/rearrange-string-k-distance-apart>  

[← Back to index](../INDEX.md)

## 1. Priority Queue

The key insight is that we should always place the character with the highest remaining frequency next. This greedy approach maximizes our chances of success because using up high-frequency characters early gives us more flexibility later.

However, after placing a character, we cannot use it again until at least `k` positions have passed. To handle this constraint, we use a "cooldown" queue that holds recently used characters along with the index where they were placed. Once enough positions have passed, the character becomes available again and returns to the priority queue.

If at any point we have no available characters to place (the priority queue is empty while we still need more characters), it means rearrangement is impossible.

```cpp
class Solution {
public:
    string rearrangeString(string s, int k) {
        int freq[26] = {0};
        // Store the frequency for each character.
        for (int i = 0; i < s.size(); i++) {
            freq[s[i] - 'a']++;
        }

        priority_queue<pair<int, int>> free;
        // Insert the characters with their frequencies in the max heap.
        for (int i = 0; i < 26; i++) {
            if (freq[i]) {
                free.push({freq[i], i});
            }
        }

        string ans;
        // This queue stores the characters that cannot be used now.
        queue<pair<int, int>>  busy;
        while (ans.size() != s.size()) {
            int index = ans.size();

            // Insert the character that could be used now into the free heap.
            if (!busy.empty() && (index - busy.front().first) >= k) {
                auto q = busy.front(); busy.pop();
                free.push({freq[q.second], q.second});
            }

            // If the free heap is empty, it implies no character can be used at this index.
            if (free.empty()) {
                return "";
            }

            int currChar = free.top().second; free.pop();
            ans += currChar + 'a';

            // Insert the used character into busy queue with the current index.
            freq[currChar]--;
            if (freq[currChar] > 0) {
                busy.push({index, currChar});
            }
        }

        return ans;
    }
};
```

**Complexity**

- Time complexity: $O((N + K) \log K)$
- Space complexity: $O(K)$

> Where $N$ is the length of the string `s`, and $K$ is the number of unique characters in the string `s`.

## 2. Greedy

Instead of simulating character placement one by one, we can think of the problem in terms of segments. If the maximum frequency of any character is `maxFreq`, we need at least `maxFreq` segments. Characters with the highest frequency must appear in every segment, while those with lower frequencies can be distributed across fewer segments.

The idea is to first place all high-frequency characters (those appearing `maxFreq` or `maxFreq - 1` times) into their respective segments, ensuring they are spaced apart. Then, distribute the remaining characters in a round-robin fashion across the first `maxFreq - 1` segments.

For the arrangement to be valid, each of the first `maxFreq - 1` segments must have at least `k` characters. The last segment can be shorter since no character needs to maintain distance after it.

```cpp
class Solution {
public:
    string rearrangeString(string s, int k) {
        unordered_map<char, int> freqs;
        int maxFreq = 0;
        // Store the frequency, and find the highest frequency.
        for (char c : s) {
            freqs[c]++;
            maxFreq = max(maxFreq, freqs[c]);
        }

        unordered_set<char> mostChars;
        unordered_set<char> secondChars;
        // Store all the characters with the highest and second highest frequency - 1.
        for (pair<char, int> charPair: freqs) {
            if (charPair.second == maxFreq) {
                mostChars.insert(charPair.first);
            } else if (charPair.second == maxFreq - 1) {
                secondChars.insert(charPair.first);
            }
        }

        // Create maxFreq number of different strings.
        string segments[maxFreq];
        // Insert one instance of characters with frequency maxFreq & maxFreq - 1 in each segment.
        for (int i = 0; i < maxFreq; i++) {
            for (char c: mostChars) {
                segments[i] += c;
            }

            // Skip the last segment as the frequency is only maxFreq - 1.
            if (i < maxFreq - 1) {
                for (char c: secondChars) {
                    segments[i] += c;
                }
            }
        }

        int segmentId = 0;
        // Iterate over the remaining characters, and for each, distribute the instances over the segments.
        for (pair<char, int> charPair: freqs) {
            char currChar = charPair.first;

            // Skip characters with maxFreq or maxFreq - 1
            // frequency as they have already been inserted.
            if (mostChars.find(currChar)  != mostChars.end()
                || secondChars.find(currChar) != secondChars.end()) {
                continue;
            }

            // Distribute the instances of these characters over the segments in a round-robin manner.
            for (int freq = freqs[currChar]; freq > 0; freq--) {
                segments[segmentId] += charPair.first;
                segmentId = (segmentId + 1) % (maxFreq - 1);
            }
        }

        // Each segment except the last should have exactly K elements; else, return "".
        for (int i = 0; i < maxFreq - 1; i++) {
            if (segments[i].size() < k) {
                return "";
            }
        }

        string ans;
        // Join all the segments and return them.
        for (string s : segments) {
            ans += s;
        }

        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(K)$

> Where $N$ is the length of the string `s`, and $K$ is the number of unique characters in the string `s`.
