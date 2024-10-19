# store columns & retrieve columns
# store contextual data and retrieve contextual data


from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from neo4j import GraphDatabase
from typing import Dict, Any, List, Optional
import uuid
# Define the FastAPI app
app = FastAPI()

# Neo4j connection configuration
NEO4J_URI = "bolt://localhost:7687"  # Update this with your Neo4j URI
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Testing123"

class Neo4jConnection:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query(self, query: str, parameters: dict = {}):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]

# Dependency to get a Neo4j connection
def get_db():
    db = Neo4jConnection(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        yield db
    finally:
        db.close()

# Pydantic model for request body
# class Person(BaseModel):
#     name: str
#     age: int

class Table(BaseModel):
    table_id: Optional[str] = None
    name: str
    dynamic_properties: Dict[str, Any] = {}

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Alice",
                "dynamic_properties": {
                    # "email": "alice@example.com",
                    # "city": "Wonderland",
                    # "phone_number": "123-456-7890"
                }
            }
        }

class Column(BaseModel):
    name: str
    contextual_description: str

    class Config:
        json_schema_extra = {
           "example": {
                "name": "price",
                "description": "This is the product price"
           }
        }

@app.post("/table/")
def create_table(table: Table, db: Neo4jConnection = Depends(get_db)):

    table_id = str(uuid.uuid4())

    query = """CREATE (p:Table {name: $name})
    SET p += $dynamic_properties
    RETURN p"""
    dynamic_properties = {k: v for k, v in table.dynamic_properties.items() if isinstance(v, (str, int, float, bool, list))}

    result = db.query(query, {"table_id": table_id, "name": table.name, "dynamic_properties": dynamic_properties})
    
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create table")
    
    return {"table_id": result[0]["p.table_id"],"name": result[0]["p.name"], "dynamic_properties": dynamic_properties}




@app.post("/columns/{table_id}")
def create_column(column: Column, db: Neo4jConnection = Depends(get_db)):
    # query = """CREATE (p:column {name: $name, contextual_description: $contextual_description})
    # """
    query = """
        match (a:Table {table_id: $table_id}) create (n:column {name: $name, contextual_description: $contextual_description})-[r:column_of]->(a) return a, n
    """
    result = db.query(query, {"name": column.name, "contextual_description": column.contextual_description})
    
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create column")
    
    return {"name": result[0]["p.name"]}



@app.get("/columns/{table_id}")
def create_column(id: int, db: Neo4jConnection = Depends(get_db)):
    query = """MATCH (c:Column) WHERE ID(c) = $id RETURN c"""
    
    result = db.query(query, {id: id})
    
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create column")
    
    return {"name": result[0]["p.name"]}



@app.delete("/column/{id}")
def create_column(id: int, db: Neo4jConnection = Depends(get_db)):
    query = """MATCH (c:Column) WHERE ID(c) = $id DELETE c"""
    
    result = db.query(query, {id: str(id)})
    
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create column")
    
    return {"name": result[0]["p.name"]}


# # Route to add a new person to the Neo4j database
# @app.post("/person/")
# def create_person(person: Person, db: Neo4jConnection = Depends(get_db)):
#     query = """
#     CREATE (p:Person {name: $name, age: $age})
#     RETURN p.name, p.age
#     """
#     result = db.query(query, {"name": person.name, "age": person.age})
    
#     if not result:
#         raise HTTPException(status_code=400, detail="Failed to create person")
    
#     return {"name": result[0]["p.name"], "age": result[0]["p.age"]}



# # Route to get all persons from the Neo4j database
# @app.get("/persons/", response_model=List[Person])
# def get_persons(db: Neo4jConnection = Depends(get_db)):
#     query = """
#     MATCH (p:Person)
#     RETURN p.name as name, p.age as age
#     """
#     result = db.query(query)
    
#     return [{"name": record["name"], "age": record["age"]} for record in result]

# # Run the server: uvicorn main:app --reload
