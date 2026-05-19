import os
from src.mst import solve, add_vertex_to_mst

def main():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "data", "islands.csv")

    edges, total_weight = solve(file_path)
    
    print("Ребра мінімального остовного дерева:")
    for u, v, weight in edges:
        print(f"  ({u},{v}) -> {weight} км")
    print(f"\nМінімальна довжина кабелів: {total_weight} км")
    
    print("\n" + "="*25)
    print("Додавання нового острова")
    print("="*25)
    
    new_island_edges = [
        (3, 0, 4),
        (3, 1, 2),  
        (3, 2, 5),
    ]
    
    print("Новий острів має з'єднання:")
    for u, v, weight in new_island_edges:
        print(f"  ({u},{v}) -> {weight} км")
    
    updated_mst = add_vertex_to_mst(edges.copy(), new_island_edges)
    
    new_total_weight = sum(weight for _, _, weight in updated_mst)
    
    print("\nОновлені ребра мінімального остовного дерева:")
    for u, v, weight in updated_mst:
        print(f"  ({u},{v}) -> {weight} км")
    print(f"\nНова мінімальна довжина кабелів: {new_total_weight} км")
    print(f"Додано: {new_total_weight - total_weight} км")


if __name__ == "__main__":
    main()