import networkx as nx
import customtkinter as ctk
import matplotlib.pyplot as plt
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
from solver import find_best_server_steps

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("700x600")
app.title("Graph Builder")

edges = []
nodes = set()
clients = set()
servers = set()

def refresh_nodes():
    nodes_label.configure(text=f"Nodes: {sorted(nodes)}")

def refresh_roles():
    server_text = f"Server: {list(servers)[0] if servers else 'None'}"
    roles_label.configure(
        text=f"Clients: {sorted(clients)} | {server_text}"
    )

node_entry = ctk.CTkEntry(app, placeholder_text="Node id")
node_entry.pack(pady=5)

def add_node():
    try:
        n = int(node_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer for Node id")
        return

    nodes.add(n)
    node_entry.delete(0, "end")
    refresh_nodes()

def on_node_enter(event):
    add_node()

node_entry.bind("<Return>", on_node_enter)
ctk.CTkButton(app, text="Add Vertex", command=add_node).pack(pady=5)

delete_node_entry = ctk.CTkEntry(app, placeholder_text="Node id to delete")
delete_node_entry.pack(pady=5)

def delete_node():
    try:
        n = int(delete_node_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer for Node id")
        return

    if n in nodes:
        nodes.discard(n)
        edges[:] = [(u, v, w) for u, v, w in edges if u != n and v != n]
        clients.discard(n)
        servers.discard(n)
        delete_node_entry.delete(0, "end")
        refresh_nodes()
        refresh_roles()

def on_delete_node_enter(event):
    delete_node()

delete_node_entry.bind("<Return>", on_delete_node_enter)
ctk.CTkButton(app, text="Delete Node", command=delete_node).pack(pady=5)

nodes_label = ctk.CTkLabel(app, text="Nodes: []")
nodes_label.pack(pady=5)

u_entry = ctk.CTkEntry(app, placeholder_text="U")
v_entry = ctk.CTkEntry(app, placeholder_text="V")
w_entry = ctk.CTkEntry(app, placeholder_text="Weight")

u_entry.pack(pady=2)
v_entry.pack(pady=2)
w_entry.pack(pady=2)

def add_edge():
    try:
        u = int(u_entry.get())
        v = int(v_entry.get())
        w = int(w_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integers for edge U, V and Weight")
        return

    if u not in nodes or v not in nodes:
        messagebox.showerror("Error", "Both edge nodes must already exist")
        return

    if w < 0:
        messagebox.showerror("Error", "Edge weight must be non-negative")
        return

    edges.append((u, v, w))
    u_entry.delete(0, "end")
    v_entry.delete(0, "end")
    w_entry.delete(0, "end")
    u_entry.focus()


def on_u_enter(event):
    v_entry.focus()

def on_v_enter(event):
    w_entry.focus()

def on_w_enter(event):
    add_edge()

u_entry.bind("<Return>", on_u_enter)
v_entry.bind("<Return>", on_v_enter)
w_entry.bind("<Return>", on_w_enter)

ctk.CTkButton(app, text="Add Edge", command=add_edge).pack(pady=5)

selected_node = ctk.CTkEntry(app, placeholder_text="Select node for role")
selected_node.pack(pady=5)

def make_client():
    try:
        n = int(selected_node.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid node id")
        return

    if n not in nodes:
        messagebox.showerror("Error", "Client node must already exist")
        return

    if n in servers:
        messagebox.showerror("Error", "Server cannot also be a client")
        return

    clients.add(n)
    selected_node.delete(0, "end")
    refresh_roles()


def make_server():
    try:
        n = int(selected_node.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid node id")
        return

    if n not in nodes:
        messagebox.showerror("Error", "Server node must already exist")
        return

    if n in clients:
        messagebox.showerror("Error", "Client cannot also be a server")
        return

    servers.clear()
    servers.add(n)
    selected_node.delete(0, "end")
    refresh_roles()

ctk.CTkButton(app, text="Make Client", command=make_client).pack(pady=2)
ctk.CTkButton(app, text="Make Server", command=make_server).pack(pady=2)

roles_label = ctk.CTkLabel(app, text="Clients: [] | Server: None")
roles_label.pack(pady=5)

def load_example_graph():
    global nodes, edges, clients, servers
    
    nodes = {1, 2, 3, 4, 5, 6}
    edges = [
        (1, 2, 10),
        (1, 3, 15),
        (2, 3, 5),
        (2, 4, 20),
        (3, 5, 8),
        (4, 5, 3),
        (4, 6, 12),
        (5, 6, 7),
    ]
    clients = {1, 5, 6}
    servers = {3}
    
    refresh_nodes()
    refresh_roles()
    messagebox.showinfo("Success", "Example graph loaded!")

def load_graph_from_file():
    global nodes, edges, clients, servers
    
    file_path = filedialog.askopenfilename(
        title="Select graph file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    
    if not file_path:
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        nodes.clear()
        edges.clear()
        clients.clear()
        servers.clear()
        
        for line in lines:
            if line.startswith('nodes:'):
                node_str = line.split(':', 1)[1].strip()
                nodes.update(int(n.strip()) for n in node_str.split(','))
            elif line.startswith('edges:'):
                edge_str = line.split(':', 1)[1].strip()
                for edge_part in edge_str.split(','):
                    edge_part = edge_part.strip()
                    if ':' in edge_part:
                        nodes_part, weight = edge_part.split(':', 1)
                        u, v = nodes_part.split('-')
                        w = int(weight.strip())
                        if w < 0:
                            raise ValueError("Negative edge weight is not allowed")
                        edges.append((int(u.strip()), int(v.strip()), w))
            elif line.startswith('clients:'):
                client_str = line.split(':', 1)[1].strip()
                clients.update(int(c.strip()) for c in client_str.split(','))
            elif line.startswith('server:'):
                server_str = line.split(':', 1)[1].strip()
                servers.add(int(server_str.strip()))
        
        refresh_nodes()
        refresh_roles()
        messagebox.showinfo("Success", f"Graph loaded from {file_path}")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load graph: {str(e)}")

def run_visualization():
    if not nodes:
        messagebox.showerror("Error", "Please add at least some nodes")
        return
    
    if not edges:
        messagebox.showerror("Error", "Please add at least some edges")
        return
    
    if not clients:
        messagebox.showerror("Error", "Please select at least one client")
        return

    sorted_nodes = sorted(nodes)
    result, steps = find_best_server_steps(sorted_nodes, list(clients), edges)
    if result == -1:
        messagebox.showerror("Error", "Cannot reach all clients from any server")
        return

    graph = nx.Graph()
    for node in nodes:
        graph.add_node(node)
    for u, v, w in edges:
        graph.add_edge(u, v, weight=w)

    pos = nx.spring_layout(graph, seed=42)
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 8))

    def draw_step(current_server, current_latency, best_server, best_latency, final=False):
        ax.clear()
        nx.draw_networkx_edges(graph, pos, ax=ax, width=2, alpha=0.6)
        edge_labels = nx.get_edge_attributes(graph, "weight")
        nx.draw_networkx_edge_labels(graph, pos, edge_labels, ax=ax)

        node_colors = []
        for node in graph.nodes():
            if final and node == best_server:
                node_colors.append("red")
            elif node == current_server:
                node_colors.append("yellow")
            elif node in clients:
                node_colors.append("green")
            else:
                node_colors.append("lightblue")

        nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=1000, alpha=0.9, ax=ax)
        nx.draw_networkx_labels(graph, pos, font_size=10, font_weight="bold", ax=ax)

        title = (
            f"Крок: тестуємо сервер {current_server}. "
            f"Макс затримка = {current_latency}. Найкраще = {best_latency}"
        )
        if final:
            title = f"Оптимальний сервер: {best_server}, затримка = {best_latency}"
        ax.set_title(title, fontsize=14, fontweight="bold")

        if not final:
            current_best_text = (
                f"Поки що найкращий сервер: {best_server}"
                if best_server is not None else
                "Поки що найкращий сервер: ще не визначено"
            )
            ax.text(
                0.02,
                0.95,
                current_best_text,
                transform=ax.transAxes,
                fontsize=12,
                color="red",
                fontweight="bold",
                ha="left",
                va="top",
                bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", boxstyle="round,pad=0.3"),
                clip_on=False,
            )

        handles = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow', markersize=10),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', markersize=10)
        ]
        labels = ['Найкращий сервер', 'Поточний сервер', 'Клієнт', 'Інше']
        ax.legend(handles, labels)
        ax.axis('off')
        fig.canvas.draw()
        plt.pause(1.5)

    best_server = None
    best_latency = float('inf')

    for server, step_latency, best_so_far in steps:
        if best_so_far < best_latency:
            best_latency = best_so_far
            best_server = server
        draw_step(server, step_latency, best_server, best_latency)

    if best_server is not None:
        servers.clear()
        servers.add(best_server)
        refresh_roles()
        draw_step(best_server, best_latency, best_server, best_latency, final=True)
    else:
        ax.set_title("Не знайдено оптимального сервера", fontsize=14, fontweight="bold")
        fig.canvas.draw()

    plt.ioff()
    plt.show()

ctk.CTkButton(app, text="Load Example Graph", command=load_example_graph).pack(pady=5)
ctk.CTkButton(app, text="Load Graph from File", command=load_graph_from_file).pack(pady=5)
ctk.CTkButton(app, text="Visualize Graph", command=run_visualization).pack(pady=5)

app.mainloop()