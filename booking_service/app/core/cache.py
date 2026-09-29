import functools
import json
from typing import Callable
from app.redis import redis_client


def cache(expire: int = 60, prefix: str = ""):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key_parts = [prefix or func.__qualname__]
            
            if len(args) > 1:
                key_parts.extend([str(a) for a in args[1:]])
                
            if kwargs:
                key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])

            cache_key = ":".join(key_parts)

            cached_data = await redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data)

            result = await func(*args, **kwargs)

            if result is not None:
                if hasattr(result, "model_dump"):
                    serializable_data = result.model_dump(mode="json")
                elif isinstance(result, list) and result and hasattr(result[0], "model_dump"):
                    serializable_data = [item.model_dump(mode="json") for item in result]
                else:
                    serializable_data = result

                await redis_client.set(
                    key=cache_key,
                    value=json.dumps(serializable_data, default=str),
                    expire=expire,
                )

            return result

        return wrapper

    return decorator