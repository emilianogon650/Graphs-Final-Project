import csv
import networkx as nx
import matplotlib.pyplot as plt
import random

# Load airport data (filter for US only)
airport_id_to_info = {}
us_airport_ids = set()

with open('/Users/emiliano.gon/Documents/Graphs Class/airports.dat.txt', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            airport_id = int(row[0])
            name = row[1].strip()
            country = row[3].strip()
            iata = row[4].strip()

            if country == "United States" and iata and iata != "\\N":
                airport_id_to_info[airport_id] = (name, country, iata)
                us_airport_ids.add(airport_id)
        except:
            continue

# Build the full US-only graph
G_full = nx.DiGraph()

with open('/Users/emiliano.gon/Documents/Graphs Class/routes.dat.txt', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            source_id = int(row[3])
            dest_id = int(row[5])
            if source_id in us_airport_ids and dest_id in us_airport_ids:
                source_name, _, source_code = airport_id_to_info[source_id]
                dest_name, _, dest_code = airport_id_to_info[dest_id]
                G_full.add_edge(source_code, dest_code)
        except:
            continue

# Find the largest strongly connected component
largest_scc = max(nx.strongly_connected_components(G_full), key=len)
connected_airports = sorted(list(largest_scc))

# Sample 50 airports from the largest SCC
random.seed(42)
sampled_airports = random.sample(connected_airports, 50)
G = G_full.subgraph(sampled_airports).copy()

# Plotting function
def plot_graph(graph, title):
    plt.figure(figsize=(14, 14))
    pos = nx.spring_layout(graph, seed=42)
    edge_weights = [graph[u][v].get('weight', 1) for u, v in graph.edges()]
    nx.draw_networkx_nodes(graph, pos, node_size=1000, node_color="skyblue")
    nx.draw_networkx_edges(graph, pos, width=edge_weights, edge_color="gray", arrowstyle="-|>", arrowsize=10)
    nx.draw_networkx_labels(graph, pos, font_size=8, font_color="black")
    plt.title(title)
    plt.axis("off")
    plt.show()

# Plot the connectivity graph
plot_graph(G, "Connectivity Among 50 US Airports")

# Most incoming flights
incoming_counts = dict(G.in_degree())
most_incoming = max(incoming_counts.items(), key=lambda x: x[1])
print(f"Most incoming flights: {most_incoming[0]} with {most_incoming[1]} incoming edges")
plot_graph(G.subgraph([most_incoming[0]] + list(G.predecessors(most_incoming[0]))),
           f"Most Incoming Flights: {most_incoming[0]}")

# Most outgoing flights
outgoing_counts = dict(G.out_degree())
most_outgoing = max(outgoing_counts.items(), key=lambda x: x[1])
print(f"Most outgoing flights: {most_outgoing[0]} with {most_outgoing[1]} outgoing edges")
plot_graph(G.subgraph([most_outgoing[0]] + list(G.successors(most_outgoing[0]))),
           f"Most Outgoing Flights: {most_outgoing[0]}")

# Floyd-Warshall: all pairs shortest paths
def floyd_warshall_all_pairs(G):
    print("Floyd-Warshall All-Pairs Shortest Paths (Number of Stops):")
    path_lengths = dict(nx.floyd_warshall(G))
    
    count = 0
    for src in path_lengths:
        for dst in path_lengths[src]:
            if src != dst and path_lengths[src][dst] < float('inf'):
                print(f"{src} → {dst}: {int(path_lengths[src][dst])} stops")
                count += 1
            if count == 5:
                return

# Visualize Floyd-Warshall results (≤ 3 stops for readability)
def visualize_all_shortest_paths(G):
    print("Generating shortest paths graph (Floyd-Warshall)...")
    fw_paths = dict(nx.floyd_warshall(G))
    shortest_path_graph = nx.DiGraph()

    for source in fw_paths:
        for target in fw_paths[source]:
            if source != target:
                distance = fw_paths[source][target]
                if distance < float('inf') and distance <= 3:
                    shortest_path_graph.add_edge(source, target, weight=1 / (distance + 1))

    print(f"Visualizing {shortest_path_graph.number_of_edges()} shortest-path edges (≤ 3 stops)")
    plot_graph(shortest_path_graph, "Floyd-Warshall: All-Pairs Shortest Paths (≤ 3 Stops)")

# Run all algorithms
floyd_warshall_all_pairs(G)
visualize_all_shortest_paths(G)




