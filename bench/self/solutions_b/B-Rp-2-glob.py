def glob_match(pattern: str, path: str) -> bool:
    pattern_segments = pattern.split("/")
    path_segments = path.split("/")

    # memoization for (pattern_idx, path_idx)
    memo = {}

    def solve(p_idx: int, s_idx: int) -> bool:
        state = (p_idx, s_idx)
        if state in memo:
            return memo[state]

        # Base case: reached end of pattern
        if p_idx == len(pattern_segments):
            # Match is successful only if we also reached end of path
            res = s_idx == len(path_segments)
            memo[state] = res
            return res

        curr_p = pattern_segments[p_idx]

        # Case 1: "**" matches zero or more entire segments
        if curr_p == "**":
            # Option A: "**" matches zero segments (move to next pattern segment)
            if solve(p_idx + 1, s_idx):
                memo[state] = True
                return True
            # Option B: "**" matches one or more segments (consume one path segment and stay on "**")
            if s_idx < len(path_segments):
                if solve(p_idx, s_idx + 1):
                    memo[state] = True
                    return True
            memo[state] = False
            return False

        # Case 2: Single segment matching
        # If we ran out of path segments but pattern still has non-"**" segments
        if s_idx == len(path_segments):
            # Only possible if remaining pattern segments are all "**"
            # But we handled "**" above. If we are here, curr_p is not "**".
            # However, a pattern like "a/**" vs "a" needs to handle the end.
            # If curr_p is not "**", it must match something.
            # But wait, if pattern is "a/**" and path is "a", 
            # p_idx 0 is "a", s_idx 0 is "a" -> match.
            # p_idx 1 is "**", s_idx 1 is end -> solve(2, 1) is True.
            # So if s_idx == len(path_segments), we can only match if curr_p is empty 
            # and we are at the end, or if we handle empty segments.
            # Actually, if s_idx == len(path_segments), the only way to match is if 
            # the pattern segment is empty (representing a trailing slash or //) 
            # and we are at the end, but that's handled by the loop.
            # Let's check if curr_p can match an empty string (only if it's empty segment)
            # but path segments are fixed. If s_idx == len(path_segments), 
            # there are no more segments to match.
            memo[state] = False
            return False

        curr_s = path_segments[s_idx]

        # Case 3: "*" matches zero or more characters (not "/")
        if curr_p == "*":
            # "*" matches zero or more characters in the current segment
            # Since we are matching segment by segment, "*" matches any string 
            # within this segment.
            # We must check if the rest of the pattern matches the rest of the path.
            # But "*" is a segment-level wildcard here? 
            # Spec: "*" matches any run (possibly empty) of characters other than "/".
            # This means "*" matches the entire current segment.
            if solve(p_idx + 1, s_idx + 1):
                memo[state] = True
                return True
            memo[state] = False
            return False

        # Case 4: "?" matches one character (not "/")
        if curr_p == "?":
            if len(curr_s) == 1:
                if solve(p_idx + 1, s_idx + 1):
                    memo[state] = True
                    return True
            memo[state] = False
            return False

        # Case 5: Literal or mixed pattern (e.g., "*.py" or "a?c")
        # The spec says: "?" matches one char, "*" matches any run, "**" matches segments.
        # It doesn't explicitly say "*" can be part of a segment like "*.py".
        # However, "src/**/*.py" example implies "*" and "?" can be part of a segment.
        # Let's implement segment-level matching for the current segment.
        
        if match_segment(curr_p, curr_s):
            if solve(p_idx + 1, s_idx + 1):
                memo[state] = True
                return True

        memo[state] = False
        return False

    def match_segment(p_seg: str, s_seg: str) -> bool:
        # Standard glob segment matching (no "/" allowed in segments)
        # p_seg can contain '*' and '?'
        n, m = len(p_seg), len(s_seg)
        dp = [[False] * (m + 1) for _ in range(n + 1)]
        dp[0][0] = True
        for i in range(1, n + 1):
            if p_seg[i-1] == '*':
                dp[i][0] = dp[i-1][0]
            else:
                dp[i][0] = False
        
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if p_seg[i-1] == '*':
                    dp[i][j] = dp[i-1][j] or dp[i][j-1]
                elif p_seg[i-1] == '?' or p_seg[i-1] == s_seg[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = False
        return dp[n][m]

    return solve(0, 0)
