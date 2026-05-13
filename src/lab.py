import os

def solve_ijones(width, height, grid):
    if width == 0:
        return 0

    dp = [[0] * width for _ in range(height)]
    
    char_sums = {}

    for r in range(height):
        dp[r][0] = 1
        char = grid[r][0]
        char_sums[char] = char_sums.get(char, 0) + 1

    for c in range(1, width):
        current_col_sums = {}

        for r in range(height):
            char = grid[r][c]
            
            ways = dp[r][c-1]
            
            
            same_char_ways = char_sums.get(char, 0)
            if grid[r][c-1] == char:
                same_char_ways -= dp[r][c-1]
            
            dp[r][c] = ways + same_char_ways
            current_col_sums[char] = current_col_sums.get(char, 0) + dp[r][c]

        for char, val in current_col_sums.items():
            char_sums[char] = char_sums.get(char, 0) + val

    res = dp[0][width - 1]
    if height > 1:
        res += dp[height - 1][width - 1]
        
    return res

def main():
    input_path = os.path.join("data", "ijones.in")
    output_path = os.path.join("data", "ijones.out")

    if not os.path.exists("data"):
        os.makedirs("data")

    try:
        with open(input_path, "r") as f:
            line = f.readline().split()
            if not line: return
            w, h = map(int, line)
            grid = [f.readline().strip() for _ in range(h)]

        result = solve_ijones(w, h, grid)

        with open(output_path, "w") as f:
            f.write(str(result))
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    main()