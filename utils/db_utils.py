# from config import DB_NAME
# from databricks import sql

# def insert_file_metadata(file_id, file_path):
#     query = f"""
#     INSERT INTO {DB_NAME}.file (fileid, filelocation)
#     VALUES ('{file_id}', '{file_path}')
#     """
#     with sql.connect() as c:
#         c.execute(query)

# def insert_page_text(file_id, page_id, text):
#     query = f"""
#     INSERT INTO {DB_NAME}.page (fileid, pageid, pagetext)
#     VALUES ('{file_id}', {page_id}, '{text}')
#     """
#     with sql.connect() as c:
#         c.execute(query)

# def insert_chunk(file_id, page_id, chunk_id, chunk, embedding):
#     query = f"""
#     INSERT INTO {DB_NAME}.chunkvector (fileid, pageid, chunkid, chunktext, embedding)
#     VALUES ('{file_id}', {page_id}, {chunk_id}, '{chunk}', {embedding})
#     """
#     with sql.connect() as c:
#         c.execute(query)
