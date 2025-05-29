import json
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

def plot_fire_state(nodes_positions, edges, burning_nodes, burned_nodes, step, protected_nodes, firefighter_position, folder):
    """
    Genera y guarda una imagen 3D del estado actual de la propagación del incendio.
    """
    fig = go.Figure()

    # Nodos en llamas (burning)
    fig.add_trace(go.Scatter3d(
        x=[nodes_positions[node, 0] for node in burning_nodes],
        y=[nodes_positions[node, 1] for node in burning_nodes],
        z=[nodes_positions[node, 2] for node in burning_nodes],
        mode='markers',
        marker=dict(size=5, color='black'),
        name='Burning Nodes'
    ))

    # Nodos quemados (burned)
    fig.add_trace(go.Scatter3d(
        x=[nodes_positions[node, 0] for node in burned_nodes],
        y=[nodes_positions[node, 1] for node in burned_nodes],
        z=[nodes_positions[node, 2] for node in burned_nodes],
        mode='markers',
        marker=dict(size=5, color='black'),
        name='Burned Nodes'
    ))

    # Nodos protegidos (protected)
    if protected_nodes:
        fig.add_trace(go.Scatter3d(
            x=[nodes_positions[node, 0] for node in protected_nodes],
            y=[nodes_positions[node, 1] for node in protected_nodes],
            z=[nodes_positions[node, 2] for node in protected_nodes],
            mode='markers',
            marker=dict(size=5, color='yellow'),
            name='Protected Nodes'
        ))

    # Nodos que no han sido quemados ni están en llamas (restantes)
    all_nodes = set(range(nodes_positions.shape[0]))
    unaffected_nodes = all_nodes - set(burning_nodes) - set(burned_nodes)

    if protected_nodes:
        unaffected_nodes = unaffected_nodes - set(protected_nodes)

    fig.add_trace(go.Scatter3d(
        x=[nodes_positions[node, 0] for node in unaffected_nodes],
        y=[nodes_positions[node, 1] for node in unaffected_nodes],
        z=[nodes_positions[node, 2] for node in unaffected_nodes],
        mode='markers',
        marker=dict(size=5, color='blue'),
        name='Unaffected Nodes'
    ))

    # Agregar aristas entre nodos
    for edge in edges:
        i, j = edge
        fig.add_trace(go.Scatter3d(
            x=[nodes_positions[i, 0], nodes_positions[j, 0]],
            y=[nodes_positions[i, 1], nodes_positions[j, 1]],
            z=[nodes_positions[i, 2], nodes_positions[j, 2]],
            mode='lines',
            line=dict(color='gray', width=2),
            showlegend=False
        ))

    # Agregar posicion del bombero
    fig.add_trace(go.Scatter3d(
        x=[firefighter_position[0]],
        y=[firefighter_position[1]],
        z=[firefighter_position[2]],
        mode='markers',
        marker=dict(size=5, color='green'),
        name='Firefighter'
    ))

    # Configuracion
    fig.update_layout(title=f'Step {step}: Fire Propagation',
                    scene=dict(xaxis=dict(title='X Axis', range=[-1, 1]),
                                yaxis=dict(title='Y Axis', range=[-1, 1]),
                                zaxis=dict(title='Z Axis', range=[-1, 1])),
                    width=700, height=700)

    # Guardar la imagen
    fig.write_image(f"{folder}{step}.png")

def plot_3d_final_state(nodes_positions, edges, burning_nodes, burned_nodes, protected_nodes, firefighter_position, folder=None, file_name=None):
    """
    Genera y guarda una imagen 3D del estado final de la propagación del incendio.
    """
    fig = go.Figure()

    # Nodos en llamas (burning)
    fig.add_trace(go.Scatter3d(
        x=[nodes_positions[node, 0] for node in burning_nodes],
        y=[nodes_positions[node, 1] for node in burning_nodes],
        z=[nodes_positions[node, 2] for node in burning_nodes],
        mode='markers',
        marker=dict(size=8, color='black'),
        name='Burning Nodes'
    ))

    # Nodos quemados (burned)
    fig.add_trace(go.Scatter3d(
        x=[nodes_positions[node, 0] for node in burned_nodes],
        y=[nodes_positions[node, 1] for node in burned_nodes],
        z=[nodes_positions[node, 2] for node in burned_nodes],
        mode='markers',
        marker=dict(size=8, color='black'),
        name='Burned Nodes'
    ))

    # Nodos protegidos (protected)
    if protected_nodes:
        fig.add_trace(go.Scatter3d(
            x=[nodes_positions[node, 0] for node in protected_nodes],
            y=[nodes_positions[node, 1] for node in protected_nodes],
            z=[nodes_positions[node, 2] for node in protected_nodes],
            mode='markers',
            marker=dict(size=8, color='yellow'),
            name='Protected Nodes'
        ))

    # Nodos que no han sido quemados ni están en llamas (restantes)
    all_nodes = set(range(nodes_positions.shape[0]))
    unaffected_nodes = all_nodes - burning_nodes - burned_nodes

    if protected_nodes:
        unaffected_nodes = unaffected_nodes - protected_nodes

    fig.add_trace(go.Scatter3d(
        x=[nodes_positions[node, 0] for node in unaffected_nodes],
        y=[nodes_positions[node, 1] for node in unaffected_nodes],
        z=[nodes_positions[node, 2] for node in unaffected_nodes],
        mode='markers',
        marker=dict(size=8, color='blue'),
        name='Unaffected Nodes'
    ))

    # Agregar aristas entre nodos
    for i in range(edges.shape[0]):
        for j in range(edges.shape[1]):
            if edges[i, j] == 1:
                fig.add_trace(go.Scatter3d(
                x=[nodes_positions[i, 0], nodes_positions[j, 0]],
                y=[nodes_positions[i, 1], nodes_positions[j, 1]],
                z=[nodes_positions[i, 2], nodes_positions[j, 2]],
                mode='lines',
                line=dict(color='gray', width=2),
                showlegend=False
                ))

    # Agregar posicion del bombero
    fig.add_trace(go.Scatter3d(
        x=[firefighter_position[0]],
        y=[firefighter_position[1]],
        z=[firefighter_position[2]],
        mode='markers',
        marker=dict(size=10, color='green'),
        name='Firefighter'
    ))

    # Configuracion
    fig.update_layout(title='Final State: Fire Propagation',
            scene=dict(xaxis=dict(title='X Axis', range=[-1, 1]),
                    yaxis=dict(title='Y Axis', range=[-1, 1]),
                    zaxis=dict(title='Z Axis', range=[-1, 1])),
            width=900, height=900)
    
    # Guardar html
    if folder and file_name:
        fig.write_html(f"{folder}{file_name}.html")
    else:
        # Save the figure as an HTML file
        fig.write_html("images/final_state.html")

def plot_graph(file_path: str, output_path: str):
    # Load data
    with open(file_path + '/positions.txt', 'r', encoding='utf-8') as f:
        positions = {}
        for line in f:
            node, x, y, z = line.split()
            positions[int(node)] = (float(x), float(y), float(z))
    
    with open(file_path + '/edges.txt', 'r', encoding='utf-8') as f:
        edges = []
        # First line is the root node, we can ignore it
        next(f)  # Skip the first line
        for line in f:
            node1, node2 = map(int, line.split())
            edges.append((node1, node2))
    
    with open(file_path + '/history.json', 'r', encoding='utf-8') as f:
        history = json.load(f)      # List of dictionaries with step data

    # Create a figure
    for step, step_data in enumerate(history):
        burning_nodes = step_data['burning_nodes']
        burned_nodes = step_data['burned_nodes']
        protected_nodes = step_data['protected_nodes']
        firefighter_position = step_data['firefighter_position']

        # Convert positions to numpy array for easier indexing
        nodes_positions = np.array([positions[i] for i in range(len(positions))])

        # Plot the current state
        plot_fire_state(nodes_positions, edges, burning_nodes, burned_nodes, step, protected_nodes, firefighter_position, output_path + '/')

plot_graph('.', '.')