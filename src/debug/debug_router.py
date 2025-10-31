from fastapi import APIRouter
import aioredis
import os

router = APIRouter(prefix="/debug", tags=["Debug"])

@router.get("/cache-keys")
async def list_cache_keys():
    redis_url = os.getenv("REDIS_URL", "redis://smartshop_redis:6379")
    redis = aioredis.from_url(redis_url, encoding="utf8", decode_responses=True)
    keys = await redis.keys("*")
    await redis.close()
    return {"cache_keys": keys}
