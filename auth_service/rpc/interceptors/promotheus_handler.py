from collections.abc import Awaitable
import time
from typing import Callable
import grpc

from rpc.metrics import REQUEST_COUNTER, REQUEST_LATENCY

class PromotheusInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(self, continuation: Callable[[grpc.HandlerCallDetails], Awaitable[grpc.RpcMethodHandler]], handler_call_details: grpc.HandlerCallDetails) -> grpc.RpcMethodHandler:
        # Increase the global request counter
        REQUEST_COUNTER.labels("total").inc()

        method_name = handler_call_details.method
        
        # Increase the request counter
        REQUEST_COUNTER.labels(method_name).inc()
        
        handler = await continuation(handler_call_details)

        if handler.unary_unary:
            original_handler = handler.unary_unary
            async def request_timer(request, context):
                start = time.perf_counter()
                try:
                    response = await original_handler(request, context)
                finally:
                    duration = time.perf_counter() - start
                    REQUEST_LATENCY.labels(method_name).observe(duration)
                return response
            
            return grpc.unary_unary_rpc_method_handler(request_timer, request_deserializer=handler.request_deserializer, response_serializer=handler.response_serializer)
        
        return handler