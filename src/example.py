def process_data(data_list):
    """
    处理数据列表，返回统计信息
    """
    if not data_list:
        return {"count": 0, "average": 0, "max": 0, "min": 0}

    total = sum(data_list)
    count = len(data_list)
    average = total / count

    return {
        "count": count,
        "average": average,
        "max": max(data_list),
        "min": min(data_list),
    }


class DataProcessor:
    def __init__(self, data):
        self.data = data

    def analyze(self):
        """分析数据并返回结果"""
        results = process_data(self.data)
        return f"分析结果: {results}"

    def validate(self):
        """验证数据有效性"""
        if not isinstance(self.data, list):
            return False
        return all(isinstance(x, (int, float)) for x in self.data)


# 示例使用
if __name__ == "__main__":
    processor = DataProcessor([10, 20, 30, 40, 50])
    print(processor.analyze())
