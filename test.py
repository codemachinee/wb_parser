import asyncio


class Sheduler_block:
    def __init__(self):
        self.block = True

    async def get_block(self):
        return self.block

    async def set_block(self, value):
        self.block = value



a = Sheduler_block()


async def main():
    print(a.block)
    print(await a.get_block())
    await a.set_block(False)
    print(a.block)
    print(a)


asyncio.run(main())