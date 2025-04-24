import csv
import networkx as nx
import matplotlib.pyplot as plt

# Maps airport ID to airport name
airport_id_to_name = {}

with open('airports.dat.txt', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            airport_id = int(row[0])
            airport_name = row[1].strip()
            airport_id_to_name[airport_id] = airport_name
        except:
            continue

G = nx.DiGraph()

with open('routes.dat.txt', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            source_id = int(row[3])
            dest_id = int(row[5])

            if source_id in airport_id_to_name and dest_id in airport_id_to_name:
                source_name = airport_id_to_name[source_id]
                dest_name = airport_id_to_name[dest_id]

                G.add_node(source_name)
                G.add_node(dest_name)
                G.add_edge(source_name, dest_name)
        except:
            continue

# Get the degree (number of edges) for each airport
degree_dict = dict(G.degree())

# Sort the airports by degree in descending order (top 10)
top_airports = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)[:10]

top_airport_names = [airport_name for airport_name, _ in top_airports]
subgraph = G.subgraph(top_airport_names)

# Plotting
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(subgraph, seed=42)

# Draw out-edges in black and in-edges in red
for u, v in subgraph.edges():
    if subgraph.has_edge(v, u):  # Bidirectional
        edge_color = "purple"
    elif u in subgraph and v in subgraph:
        edge_color = "black"  # Outgoing
    else:
        edge_color = "red"  # Incoming
    nx.draw_networkx_edges(subgraph, pos, edgelist=[(u, v)], edge_color=edge_color, arrowstyle="-|>", arrowsize=15)

nx.draw_networkx_nodes(subgraph, pos, node_size=2000, node_color="skyblue")
nx.draw_networkx_labels(subgraph, pos, font_size=8, font_weight="bold")
plt.title("Directed Routes Between Top 10 Airports")
plt.show()

# Check if there's a path from Los Angeles to Munich
source_airport = "Los Angeles International Airport"
dest_airport = "Munich Airport"

if source_airport in G and dest_airport in G:
    path_exists = nx.has_path(G, source_airport, dest_airport)
    print(f"Can you travel from {source_airport} to {dest_airport}? {'Yes' if path_exists else 'No'}")
else:
    print("One or both airports not found in the graph.")