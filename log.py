import logging
import functools

# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # 输出到文件
        logging.StreamHandler()  # 输出到控制台
    ]
)

# 获取日志记录器
logger = logging.getLogger(__name__)

# 包装函数用于记录日志
def log_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_args = f"args: {args}, kwargs: {kwargs}"
        logger.info(
            f"triggered function '{func.__name__}' with {func_args}")
        return func(*args, **kwargs)
    return wrapper