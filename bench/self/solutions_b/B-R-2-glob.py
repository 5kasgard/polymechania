def glob_match(pattern: str, path: str) -> bool:
    pattern_segments = pattern.split("/")
    path_segments = path.split("/")

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

        p_seg = pattern_segments[p_idx]

        # Case 1: "**" matches zero or more entire segments
        if p_seg == "**":
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
            # But we handled "**" above. If we are here, p_seg is not "**".
            # However, we must check if the remaining pattern is just empty segments or something else.
            # Actually, if p_seg is not "**", it must match something. 
            # If s_idx == len(path_segments), it can only match if p_seg is empty and we are at the end.
            # But we already checked p_idx == len(pattern_segments).
            # The only way to match an empty path segment is if p_seg is "" and s_idx is at the end.
            # But if s_idx is at the end, we can't match a segment.
            # Exception: if p_seg is "" and we are at the end of path? No, split("/") on "" is [''].
            # Let's re-evaluate: if s_idx == len(path_segments), we can only match if p_seg is "" 
            # AND we are at the very last segment of the pattern.
            # Wait, the split logic: "a/".split("/") -> ["a", ""]. "" is a segment.
            # If s_idx == len(path_segments), we have no more segments to match.
            memo[state] = False
            return False

        s_seg = path_segments[s_idx]

        # Case 3: "*" matches any run of characters (except "/")
        if p_seg == "*":
            # "*" matches the whole segment s_seg and we move to next segment
            res = solve(p_idx + 1, s_idx + 1)
            memo[state] = res
            return res

        # Case 4: "?" matches exactly one character (except "/")
        if p_seg == "?":
            if len(s_seg) == 1:
                res = solve(p_idx + 1, s_idx + 1)
                memo[state] = res
                return res
            else:
                memo[state] = False
                return False

        # Case 5: Literal match (including empty segments and "?", "*" logic within segment)
        # The spec says "?" and "*" match characters *other than "/"*. 
        # Since we split by "/", the segments themselves do not contain "/".
        # However, the spec says "?" matches one character and "*" matches any run.
        # It does NOT say "?" and "*" are limited to segment-level matching, 
        # but the context of "a/c" vs "a?c" implies they are segment-level or character-level.
        # Re-reading: "a?c" matches "a/c" is False. This means "?" does not match "/".
        # Since we split by "/", "?" and "*" must be handled within the segment.
        
        # Let's refine: The pattern segments can contain "?" and "*".
        # Example: "src/*.py" -> segments ["src", "*.py"].
        # "src/x/a.py" -> segments ["src", "x", "a.py"].
        # This means my segment-based approach needs to handle "?" and "*" inside segments.
        
        # Let's use a helper to match a single segment.
        def match_segment(pat: str, seg: str) -> bool:
            # Standard glob segment matching (no "/" allowed in segment)
            # Since we split by "/", we know neither contains "/"
            m = len(pat)
            n = len(seg)
            dp = [[False] * (n + 1) for _ in range(m + 1)]
            dp[0][0] = True
            for i in range(1, m + 1):
                if pat[i-1] == '*':
                    dp[i][0] = dp[i-1][0]
                else:
                    dp[i][0] = False
            
            for i in range(1, m + 1):
                for j in range(1, n + 1):
                    if pat[i-1] == '*':
                        dp[i][j] = dp[i-1][j] or dp[i][j-1]
                    elif pat[i-1] == '?' or pat[i-1] == seg[j-1]:
                        dp[i][j] = dp[i-1][j-1]
                    else:
                        dp[i][j] = False
            return dp[m][n]

        # If p_seg is not "**", it must match s_seg exactly via segment rules
        if match_segment(p_seg, s_seg):
            res = solve(p_idx + 1, s_idx + 1)
            memo[state] = res
            return res
        else:
            memo[state] = False
            return False

    return solve(0, 0)
