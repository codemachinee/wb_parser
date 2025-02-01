class Sheduler_block:
    def __init__(self):
        self.news = True
        self.warehouses = True

    async def get_news(self):
        return self.news

    async def set_news(self, value):
        self.news = value

    async def get_warehouses(self):
        return self.warehouses

    async def set_warehouses(self, value):
        self.warehouses = value


sheduler_block_value = Sheduler_block()