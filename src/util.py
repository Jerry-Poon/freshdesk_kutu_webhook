from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, func, select
from sqlalchemy.orm import Session
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO)


class dbConnector:
    def __init__(self, db_name: str, db_user: str, db_password: str, db_host: str, db_port: str):
        self.engine=create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}', echo=False)
        self.cnx = self.engine.connect()

    async def getTableData(self, table_name: str) -> pd.DataFrame:
        return pd.read_sql(f'SELECT * FROM {table_name}', self.cnx)
    
    async def insertTableData(self, table_name: str, df: pd.DataFrame) -> None:
        return df.to_sql(name=table_name, con=self.cnx, if_exists='append', index=False)
    
    async def test_query(self, target_table):
        table_object = Table(target_table, MetaData(),autoload_replace=True, autoload_with=self.engine)


        # Conection Test
        with Session(self.engine) as session:
            try:
                row_count = session.query(table_object.c.order_number).count()
                logging.info(f'row count: {row_count}')
            except Exception as e:
                logging.WARNING(f'Error: {e}')
                raise e

            