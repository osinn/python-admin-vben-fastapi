import time
from core.framework.snowflake.source import options, generator, idregister

class Snowflake:
    _instance = None

    def __new__(cls, worker_id: int = 23):
        """控制实例创建"""
        if cls._instance is None:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance
    def __init__(self, worker_id: int):
        """
        初始化
        :param worker_id: 机器ID
        如果超过50W个/s，接近500W个/s，推荐修改：SeqBitLength=12
        总之，增加 SeqBitLength 会让性能更高，但生成的 ID 会更长。
        """
        if not self._instance._initialized:
            # 声明id生成器参数，需要自己构建一个worker_id，WorkerId，是区分不同机器或不同应用的唯一ID，最大值由 WorkerIdBitLength（默认6）限定
            options2 = options.IdGeneratorOptions(worker_id=worker_id, worker_id_bit_length=12, seq_bit_length=12)
            idgen = generator.DefaultIdGenerator()
            idgen.set_id_generator(options2)
            self.idgen = idgen

    def _current_millis(self):
        return int(time.time() * 1000)

    def generate_id(self):
       return self.idgen.next_id()

snowflake = Snowflake(worker_id=23)

__all__ = ["snowflake"]

# 示例用法
if __name__ == "__main__":
    # 生成ID测试
    start_time = time.time()
    for i in range(4000000):
        try:
            uid = snowflake.generate_id()
        except Exception as e:
            print(f"生成ID失败: {e}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"耗时: {elapsed_time:.6f}秒")
    print(f"耗时: {elapsed_time * 1000:.2f}毫秒")