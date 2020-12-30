from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import db

BASE_PATH = "/api"
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get(BASE_PATH)
async def root():
    return {"message": "Hello World"}


# ---------- knowledge ----------

# 知识对象
class Knowledge(BaseModel):
    code: Optional[int] = None
    name: Optional[str] = None
    type: Optional[int] = None


# 添加综合数据库
@app.post(BASE_PATH + "/knowledge/save")
async def knowledge_add(knowledge: Knowledge):
    conn = db.conn()
    # 如何已经存在就不用再添加了
    result = db.select(conn, "select * from t_code where name = ?", (knowledge.name,))
    if result is not None:
        return {"code": "-1", "message": "the name is already exist, please change a new one"}
    db.execute(conn, "insert into t_code(name, type) values (?, ?)", (knowledge.name, knowledge.type))
    db.close(conn)
    return {"code": "0", "message": "success"}


# 单条查询综合数据库
@app.post(BASE_PATH + "/knowledge/select")
async def knowledge_select(knowledge: Knowledge):
    conn = db.conn()
    # 查看添加对象是否存在
    result = db.select(conn, "select * from t_code where code = ?", (knowledge.code,))
    if result is None:
        return {"code": "-1", "message": "record is not exist"}
    db.close(conn)
    return {"code": "0", "message": "success", "data": {"code": result[0], "name": result[1], "type": result[2]}}


# 更新综合数据库
@app.post(BASE_PATH + "/knowledge/update")
async def knowledge_update(knowledge: Knowledge):
    conn = db.conn()
    # 查看编辑对象是否存在
    result = db.select(conn, "select * from t_code where code = ?", (knowledge.code,))
    if result is None:
        return {"code": "-1", "message": "record is not exist"}

    temp = db.select(conn, "select * from t_code where name = ?", (knowledge.name,))
    if temp is not None and result.code != temp.code:
        return {"code": "-1", "message": "the name is already exist, pls change a new one"}

    db.execute(conn, "update t_code set name = ?, type = ? where code = ? ",
               (knowledge.name, knowledge.type, knowledge.code))
    db.close(conn)
    return {"code": "0", "message": "success"}


# 删除综合数据库
@app.post(BASE_PATH + "/knowledge/delete")
async def knowledge_delete(knowledge: Knowledge):
    conn = db.conn()
    # 查看添加对象是否存在
    result = db.select(conn, "select * from t_code where code = ?", (knowledge.code,))
    if result is None:
        return {"code": "-1", "message": "record is not exist"}
    db.execute(conn, "delete from t_code where code = ?", (knowledge.code,))
    db.close(conn)
    return {"code": "0", "message": "success"}


# 查询全部的综合数据库列表
@app.post(BASE_PATH + "/knowledge/all")
async def knowledge_all():
    conn = db.conn()
    # 查询全部代码
    result = db.many(conn, "select * from t_code", ())
    rows = []
    if result is not None:
        for row in result:
            rows.append({"code": row[0], "name": row[1], "type": row[2]})
    db.close(conn)
    return {"code": "0", "message": "success", "data": rows}


# ---------- rule ----------

# 规则对象
class Rule(BaseModel):
    code: Optional[int] = None
    name: Optional[str] = None
    position: Optional[int] = None
    type: Optional[int] = None
    rule: Optional[str] = None


# 添加规则对象
@app.post(BASE_PATH + "/rule/save")
async def rule_add(rule: Rule):
    conn = db.conn()
    # 如何已经存在就不用再添加了
    result = db.select(conn, "select * from t_rule where name = ?", (rule.name,))
    if result is not None:
        return {"code": "-1", "message": "the name is already exist, please change a new one"}
    db.execute(conn, "insert into t_rule(name, position, type, rule) values (?, ?, ?, ?)",
               (rule.name, rule.position, rule.type, rule.rule))
    db.close(conn)
    return {"code": "0", "message": "success"}


# 单条查询规则对象
@app.post(BASE_PATH + "/rule/select")
async def rule_select(rule: Rule):
    conn = db.conn()
    # 查看添加对象是否存在
    result = db.select(conn, "select * from t_rule where code = ?", (rule.code,))
    if result is None:
        return {"code": "-1", "message": "record is not exist"}
    db.close(conn)
    return {"code": "0", "message": "success",
            "data": {"code": result[0], "name": result[1], "position": result[2], "type": result[3], "rule": result[4]}}


# 更新规则对象
@app.post(BASE_PATH + "/rule/update")
async def rule_update(rule: Rule):
    conn = db.conn()
    # 查看编辑对象是否存在
    result = db.select(conn, "select * from t_rule where code = ?", (rule.code,))
    if result is None:
        return {"code": "-1", "message": "record is not exist"}

    temp = db.select(conn, "select * from t_rule where name = ?", (rule.name,))
    if temp is not None and result.code != temp.code:
        return {"code": "-1", "message": "the name is already exist, pls change a new one"}

    db.execute(conn, "update t_rule set name = ?, position = ?, type = ? where code = ? ",
               (rule.name, rule.position, rule.type, rule.code))
    db.close(conn)
    return {"code": "0", "message": "success"}


# 删除规则对象
@app.post(BASE_PATH + "/rule/delete")
async def rule_delete(rule: Rule):
    conn = db.conn()
    # 查看添加对象是否存在
    result = db.select(conn, "select * from t_rule where code = ?", (rule.code,))
    if result is None:
        return {"code": "-1", "message": "record is not exist"}
    db.execute(conn, "delete from t_rule where code = ?", (rule.code,))
    db.close(conn)
    return {"code": "0", "message": "success"}


# 查询全部的综合数据库列表
@app.post(BASE_PATH + "/rule/all")
async def rule_all():
    conn = db.conn()
    # 查询全部代码
    result = db.many(conn, "select * from t_rule", ())
    rows = []
    if result is not None:
        for row in result:
            rows.append({"code": row[0], "name": row[1], "position": row[2], "type": row[3], "rule": row[4]})
    db.close(conn)
    return {"code": "0", "message": "success", "data": rows}
