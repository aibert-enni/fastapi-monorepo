from prometheus_client import Counter, Histogram


REQUEST_COUNTER = Counter(
    "grpc_requests_total",
    "Total number of gRPC requests",
    ["method", "status"]
)

REQUEST_LATENCY = Histogram(
    "grpc_request_latency_seconds",
    "Histogram of gRPC request latencies",
    ["method"]
)