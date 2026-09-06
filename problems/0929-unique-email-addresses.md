# 929. Unique Email Addresses

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/unique-email-addresses/>  
- **NeetCode:** <https://neetcode.io/problems/unique-email-addresses>  
- **Video:** <https://www.youtube.com/watch?v=TC_xLIWl7qY>  

[← Back to index](../INDEX.md)

## 1. Built-In Functions

Each email consists of a local name and domain separated by `@`. For the local name, periods are ignored and everything after `+` is discarded. The domain remains unchanged. Two emails are the same if they resolve to the same address after applying these rules.

We can leverage built-in string functions to parse and normalize each `e` mail, then use a set to count unique addresses.

```cpp
class Solution {
public:
    int numUniqueEmails(vector<string>& emails) {
        unordered_set<string> unique;

        for (string e : emails) {
            string local = e.substr(0, e.find('@'));
            local = local.substr(0, local.find('+'));
            local.erase(remove(local.begin(), local.end(), '.'), local.end());
            unique.insert(local + e.substr(e.find('@')));
        }
        return unique.size();
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n)$

> Where $n$ is the number of strings in the array, and $m$ is the average length of these strings.

## 2. Iteration

Instead of using built-in string functions, we can manually iterate through each character of the email. This gives us more control and can be slightly more efficient since we process each character exactly once.

```cpp
class Solution {
public:
    int numUniqueEmails(vector<string>& emails) {
        unordered_set<string> unique;

        for (string e : emails) {
            int i = 0;
            string local = "";
            while (i < e.length() && e[i] != '@' && e[i] != '+') {
                if (e[i] != '.') {
                    local += e[i];
                }
                i++;
            }

            while (i < e.length() && e[i] != '@') {
                i++;
            }
            string domain = e.substr(i + 1);
            unique.insert(local + "@" + domain);
        }
        return unique.size();
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n)$

> Where $n$ is the number of strings in the array, and $m$ is the average length of these strings.

## Standalone solution file (`cpp/0929-unique-email-addresses.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int numUniqueEmails(vector<string>& emails) {
        set<string> unique_emails;
        for(string email: emails) {
            string local_name = email.substr(0, email.find('@'));
            local_name = local_name.substr(0, email.find('+'));
            local_name = regex_replace(local_name, regex("\\."), "");
            string domain_name = email.substr(email.find('@') + 1, email.length());
            email = local_name + '@' + domain_name;
            unique_emails.insert(email);
        }
        return unique_emails.size();
    }
};
```
