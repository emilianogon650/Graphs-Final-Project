import csv
import networkx as nx
import matplotlib.pyplot as plt
import random

# Load airport data (filter for US only)
airport_id_to_info = {}  # {id: (name, country, IATA)}
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

# Sort the airports to make the result of random.sample consistent
connected_airports = sorted(list(largest_scc))

# Set a fixed seed to ensure reproducibility
random.seed(42)
sampled_airports = random.sample(connected_airports, 50)

# Create the final subgraph from those 50 fixed airports
G = G_full.subgraph(sampled_airports).copy()



def plot_graph(graph, title):
    plt.figure(figsize=(14, 14))
    pos = nx.spring_layout(graph, seed=42)
    nx.draw_networkx_nodes(graph, pos, node_size=1000, node_color="skyblue")
    nx.draw_networkx_edges(graph, pos, arrowstyle="-|>", arrowsize=10, edge_color="gray")
    nx.draw_networkx_labels(graph, pos, font_size=8, font_color="black")
    plt.title(title)
    plt.axis("off")
    plt.show()

plot_graph(G, "Connectivity Among 50 US Airports")

incoming_counts = dict(G.in_degree())
most_incoming = max(incoming_counts.items(), key=lambda x: x[1])
print(f"Most incoming flights: {most_incoming[0]} with {most_incoming[1]} incoming edges")
plot_graph(G.subgraph([most_incoming[0]] + list(G.predecessors(most_incoming[0]))),
           f"Most Incoming Flights: {most_incoming[0]}")

outgoing_counts = dict(G.out_degree())
most_outgoing = max(outgoing_counts.items(), key=lambda x: x[1])
print(f"Most outgoing flights: {most_outgoing[0]} with {most_outgoing[1]} outgoing edges")
plot_graph(G.subgraph([most_outgoing[0]] + list(G.successors(most_outgoing[0]))),
           f"Most Outgoing Flights: {most_outgoing[0]}")



