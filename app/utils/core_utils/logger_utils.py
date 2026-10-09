from functools import wraps
from app.config import logger

def log_node(func):
    """Decorator to automatically log node entry, execution details, and errors."""
    @wraps(func)
    def wrapper(state, *args, **kwargs):
        node_name = func.__name__
        logger.info("="*30)
        logger.info(f"[{node_name}]: Starting execution...")
        try:
            result = func(state, *args, **kwargs)
            logger.info(f"[{node_name}]: Completed successfully.")
            logger.info("="*30)
            return result
        except Exception as e:
            logger.error(f"[{node_name}]: Failed with error: {str(e)}", exc_info=True)
            logger.info("="*30)
            raise e
    return wrapper