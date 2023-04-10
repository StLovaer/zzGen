from typing import get_type_hints
from functools import wraps
from inspect import getfullargspec
import numpy as np
import random
 
# 定义函数参数类型的检查函数
def parameter_check(obj, **kwargs):
    hints = get_type_hints(obj)
    for label_name, label_type in hints.items():
        # print(label_name)
        # print(label_type)
        # 返回类型不检查 跳过 只检查实际传入参数的类型是否正确
        if label_name == "return":
            continue
        # 判断实际传入的参数是否与函数标签中的参数一致
        if not isinstance(kwargs[label_name], label_type):
            print(f"参数：{label_name} 类型错误 应该为：{label_type}")

# 使用装饰器进行函数包裹
def wrapped_func(decorator):
    @wraps(decorator)
    def wrapped_decorator(*args, **kwargs):
        func_args = getfullargspec(decorator)[0]
        kwargs.update(dict(zip(func_args, args)))
        parameter_check(decorator, **kwargs)
        return decorator(**kwargs)
    return wrapped_decorator

@wrapped_func
def add0(a: int, b: int) -> int:
    return a + b


@wrapped_func
def add1(a: int, b: float = 520.1314) -> float:
    return a + b

# Random sampling in a given probability distribution graph
# ---- return the position(i.e. l+index) corresponding to the sample num.
def rand_num_sampling(l,r,pdg):
    if r-l+1 != len(pdg):
        print("l is "+str(l)+" r is "+str(r)+" and pdg is "+str(pdg))
        print("error : pdg not match [l,r]")
        return l-1
    one_=sum(pdg)
    if abs(one_-1.0)>1e-5:
        print("error : probability sum "+str(one_)+" do not equal 1")
        return l-1
    pdg_=np.array(pdg)
    pdg_=[round(i*1000) for i in pdg_]
    maxv=sum(pdg_)
    num=random.randint(0,maxv-1)
    index=0
    for i in range(len(pdg_)):
        num=num-pdg_[i]
        if num<0:
            index=i
            break
    return l+index

def rand_str_sampling(str_len=16):
    random_str =''
    base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length =len(base_str) -1
    for i in range(str_len):
        random_str +=base_str[random.randint(0, length)]
    return random_str
