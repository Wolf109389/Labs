def get_next_state(pattern, m, state, x):
    if state < m and x == ord(pattern[state]):
        return state + 1

    for next_state in range(state, 0, -1):
        if ord(pattern[next_state - 1]) == x:
            if pattern[:next_state - 1] == pattern[state - next_state + 1:state]:
                return next_state
    return 0

def build_transition_table(pattern):
    m = len(pattern)
    tf = []
    for state in range(m + 1):
        tf.append({})
        chars = set(pattern)
        for char in chars:
            tf[state][char] = get_next_state(pattern, m, state, ord(char))
    return tf

def search_finite_automaton(haystack, needle):
    if not needle:
        return []

    m = len(needle)
    n = len(haystack)
    tf = build_transition_table(needle)
    
    indices = []
    state = 0
    for i in range(n):
        state = tf[state].get(haystack[i], 0)
        
        if state == m:
            indices.append(i - m + 1)
            
    return indices

if __name__ == "__main__":
    haystack_text = "aaaabaaa"
    needle_text = "aaa"
    result = search_finite_automaton(haystack_text, needle_text)

    print(f"Індекси входжень: {result}")