from src.database.db_config import DBData
from src.entities.entities import DBConnection
import aiomysql


class MySqlConnection(DBConnection):
    __pool = None

    @staticmethod
    async def _create_pool():
        MySqlConnection.__pool = await aiomysql.create_pool(**DBData.db_info)

    @staticmethod
    async def get_pool():
        if not MySqlConnection.__pool:
            await MySqlConnection._create_pool()
        return MySqlConnection.__pool

    @staticmethod
    async def close(self):
        if MySqlConnection.__pool:
            MySqlConnection.__pool.close()
            await self.pool.wait_closed()
            MySqlConnection.__pool = None


class MySqlCommands:
    def __init__(self):
        self.__pool = None

    async def __create_pool(self):
        self.__pool = await MySqlConnection.get_pool()

    async def _create(self, query: str, params: tuple|None = None):
        if not self.__pool:
            await self.__create_pool()

        async with self.__pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)

    async def _read(self, query: str, params: tuple|None = None):
        if not self.__pool:
            await self.__create_pool()

        async with self.__pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)
                result = await cur.fetchall()
                return result

    async def _update(self, query: str, params: tuple|None = None):
        if not self.__pool:
            await self.__create_pool()

        async with self.__pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)

    async def _delete(self, query: str, params: tuple|None = None):
        if not self.__pool:
            await self.__create_pool()

        async with self.__pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)


class DonorCommands(MySqlCommands):

    def __init__(self):
        super().__init__()

    async def read_donors(self):
        response = await super()._read(
            "SELECT DISTINCT Donors.id, Tags.name, Donors.name FROM Donors JOIN Tags ON Donors.tag_id = Tags.id"
        )

        return response

    async def delete_donor(self, donor_id: int):
        await super()._delete(
            "DELETE FROM Donors WHERE id = %s",
            (donor_id,)
        )

    async def add_donor(self, donor_id: int, donor_name: str, tag_id: int):
        await super()._create(
            "INSERT INTO Donors (id, name, tag_id) VALUES (%s, %s, %s)",
            (donor_id, donor_name, tag_id)
        )


class ReceiversCommands(MySqlCommands):

    def __init__(self):
        super().__init__()

    async def read_receivers(self):
        response = await super()._read(
            "SELECT DISTINCT Receivers.id, Tags.name, Receivers.name FROM Receivers JOIN Tags ON Receivers.tag_id = Tags.id"
        )

        return response

    async def delete_receiver(self, receiver_id: int):
        await super()._delete(
            "DELETE FROM Receivers WHERE id = %s",
            (receiver_id,)
        )

    async def add_receiver(self, receiver_id: int, receiver_name: str, tag_id: int):
        await super()._create(
            "INSERT INTO Receivers (id, name, tag_id) VALUES (%s, %s, %s)",
            (receiver_id, receiver_name, tag_id)
        )

    async def get_receivers_by_tag(self, tag_id: int):
        response = await super()._read(
            "SELECT id FROM Receivers WHERE tag_id = %s",
            (tag_id,)
        )
        return [i[0] for i in response]


class TagsCommands(MySqlCommands):

    def __init__(self):
        super().__init__()

    async def read_tags(self):
        response = await super()._read(
            "SELECT DISTINCT Tags.id, Tags.name FROM Tags"
        )

        return response

    async def delete_tag(self, tag_id: int):
        await super()._delete(
            "DELETE FROM Donors WHERE tag_id = %s",
            (tag_id,)
        )
        await super()._delete(
            "DELETE FROM Tags WHERE id = %s",
            (tag_id,)
        )

    async def create_tag(self, tag_name: str):
        await super()._create(
            "INSERT INTO Tags (name) VALUES (%s)",
            (tag_name,)
        )
