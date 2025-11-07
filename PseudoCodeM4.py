def update_ewma(server, latency, alpha=0.3):
    server.ewma_latency = alpha * latency + (1 - alpha) * server.ewma_latency

def select_backend(backend_servers):
    best_server = None
    best_score = float('inf')
    for server in backend_servers:
        if server.ewma_latency < best_score and server.status == 'healthy':
            best_score = server.ewma_latency
            best_server = server
    return best_server


def compute_load_score(server):
    return (
        0.5 * server.ewma_latency +
        0.3 * server.cpu_percent +
        0.2 * server.active_connections
    )