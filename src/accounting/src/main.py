from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.accounting.src.api.routers import router
from src.accounting.src.infrastructure.database.session import create_db_and_tables
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)

