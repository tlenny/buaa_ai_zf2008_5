from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import db

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello World"}


# ---------- knowledge ----------

# 知识对象
class Knowledge(BaseModel):
    code: Optional[int] = None
    name: Optional[str] = None
    type: Optional[int] = None


# 添加综合数据库
@app.post("/knowledge/save")
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
@app.post("/knowledge/select")
async def knowledge_select(knowledge: Knowledge):
    conn = db.conn()
    # 查看添加对象是否存在
    result = db.select(conn, "select * from t_code where code = ?", (knowledge.code,))
    if result is None:
        return {"code": "-1", "message": "record is not exist"}
    db.close(conn)
    return {"code": "0", "message": "success", "data": {"code": result[0], "name": result[1], "type": result[2]}}


# 更新综合数据库
@app.post("/knowledge/update")
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
@app.post("/knowledge/delete")
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
@app.post("/knowledge/all")
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
@app.post("/rule/save")
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
@app.post("/rule/select")
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
@app.post("/rule/update")
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
@app.post("/rule/delete")
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
@app.post("/rule/all")
async def rule_all():
    conn = db.conn()
    # 查询全部代码
    result = db.many(conn, "select * from t_rule order by position", ())
    rows = []
    if result is not None:
        for row in result:
            rows.append({"code": row[0], "name": row[1], "position": row[2], "type": row[3], "rule": row[4]})
    db.close(conn)
    return {"code": "0", "message": "success", "data": rows}


# ---------- process ----------

# 规则对象
class SubmitRule(BaseModel):
    rule: str


# 推理机开发
@app.post("/process")
async def process(rule: Rule):
    inputs = rule.rule.split("+")
    if len(inputs) == 0:
        return {"code": "-1", "message": "rule is not correct"}

    rules = get_rules()
    # python 不支持 do..while, 假定能匹配上
    flag = 1
    while flag == 1:
        flag = match(rules, inputs)

    if flag == 2:
        data = select_knowledge(inputs[-1])
    else:
        data = {"code": -1, "name": "无匹配动物", "type": -1}

    return {"code": "0", "message": "success", "data": data}


# 进行匹配
def match(rules, inputs):
    # 0:未匹配 1:匹配了中间结果 2:匹配到了最终结果
    flag = 0
    for rule in rules:
        array = rule["rule"].split("=")
        left = array[0]
        right = array[1]
        left_array = left.split("+")
        # 计数匹配
        match_count = 0
        # 标记匹配元素的下标，后面好删除
        match_index = []
        for i, left_value in enumerate(left_array):
            for j, value in enumerate(inputs):
                # 如果输入值有和规则库中定义一样的
                if value == left_value:
                    match_count = match_count + 1
                    match_index.append(j)
        # 如果有匹配成功的，删除匹配的节点
        if match_count == len(left_array):
            flag = 1
            # 对数据排序
            match_index.sort(reverse=True)
            for index in match_index:
                # 删除逻辑有问题
                inputs.pop(index)
            # 然后再把匹配的记录加进去
            if right not in inputs:
                inputs.append(right)
            # 判断是不是最终匹配
            if rule["type"] == 1:
                flag = 2
    return flag


# 得到所有的规则
def get_rules():
    conn = db.conn()
    # 查询全部代码
    result = db.many(conn, "select * from t_rule order by position", ())
    rows = []
    if result is not None:
        for row in result:
            rows.append({"code": row[0], "name": row[1], "position": row[2], "type": row[3], "rule": row[4]})
    db.close(conn)
    return rows


# 单条查询规则对象
def select_knowledge(code):
    conn = db.conn()
    # 查看添加对象是否存在
    result = db.select(conn, "select * from t_code where code = ?", (code,))
    if result is None:
        return {"code": "-1", "message": "record is not exist"}
    db.close(conn)
    return {"code": result[0], "name": result[1], "type": result[2]}


# 单元测试
if __name__ == '__main__':
    _inputs = "1+9+12".split("+")
    # _inputs = "4+19".split("+")
    _rules = get_rules()
    # python 不支持 do..while, 假定能匹配上
    _flag = 1
    while _flag == 1:
        print("inputs is: " + str(_inputs))
        _flag = match(_rules, _inputs)

    if _flag == 2:
        data = select_knowledge(_inputs[-1])
    else:
        data = {"code": -1, "name": "无匹配动物", "type": -1}
    print(data)
