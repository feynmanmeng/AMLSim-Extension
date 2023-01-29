import neo4j

database = 'tmp'

def create_clear(tx):
    tx.run("match (n)"
           "detach delete n")

def process_clear():
    uri = "neo4j://localhost:7687"
    driver = neo4j.GraphDatabase.driver(uri, auth=("neo4j", "key"))
    with driver.session(database=database) as session:
        session.write_transaction(create_clear)
    driver.close()
    print("已清空")

if __name__ == '__main__':
    process_clear()




