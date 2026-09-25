from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app=FastAPI(title="Advanced Python Async API",version="1.0.0")

class Item(BaseModel):
    name:str=Field(min_length=2,max_length=80)
    price:float=Field(gt=0)
    tags:list[str]=[]

items=[{"id":1,"name":"Python Course","price":49.0,"tags":["python","async"]}]

@app.get("/health")
async def health(): return {"status":"ok"}

@app.get("/items")
async def list_items(page:int=Query(1,ge=1),limit:int=Query(10,ge=1,le=100)):
    start=(page-1)*limit
    return {"page":page,"limit":limit,"total":len(items),"items":items[start:start+limit]}

@app.post("/items",status_code=201)
async def create_item(item:Item):
    record={"id":len(items)+1,**item.model_dump()}
    items.append(record)
    return record

@app.get("/items/{item_id}")
async def get_item(item_id:int):
    for item in items:
        if item["id"]==item_id:return item
    raise HTTPException(404,"Item not found")
