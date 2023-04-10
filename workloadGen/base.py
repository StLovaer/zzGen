from util import *
from schema import *

# data access distribution
class feature:
    def __init__(self,workloadSize,rwRatio,averageTableNum,tableDistribution,\
        queryComparisonOperatorRatio,tableDomainDist,queryLogicPredicateNum,\
            averageAggregationOperatorNum,averageQueryColomnNum,groupByRatio,descOrAsc) -> None:
        self.workloadSize=workloadSize # feature1
        self.rwRatio=rwRatio # feature2
        self.averageTableNum=averageTableNum # feature3
        self.tableDistribution=tableDistribution # feature4
        self.queryComparisonOperatorRatio = queryComparisonOperatorRatio # feature5
        self.tableDomainDist = tableDomainDist # feature6
        self.queryLogicPredicateNum = queryLogicPredicateNum # feature7
        self.averageAggregationOperatorNum=averageAggregationOperatorNum # feature8
        self.averageQueryColomnNum=averageQueryColomnNum # feature9
        self.groupByRatio=groupByRatio # feature10
        self.descOrAsc=descOrAsc # feature11
        
# feature1  : size of workload
# feature2  : read/write ratio
# feature3  : average table num
# feature4  : table data distribution
    # tb_choice=self.dbs.tables[randNumGen(0,len(self.dbs.tables)-1,condition.avgtb)]
    # tb_choice=get1Table(self.dbs.tables,np.full(len(self.dbs.tables),1.0/len(self.dbs.tables)))
# feature5  : different query comparison constraint ratio
    # cons=randNumGen(0,3,condition.feature4)
# feature6  : query data domain distribution
    # data=randNumGen(0,99,[1.0/100 for i in range(100)])
# feature7  : query logic predicate num
# feature8  : average aggregation operator num
# feature9  : average query colomn num
# feature10 : group by ratio
# feature11 : if ordered, desc or asc
        
import json

def load_json(filePath,mode):
    jsonFile = open(filePath,mode)
    input = json.loads(jsonFile.read())
    # print(input)
    all_tables = []
    foreign_cons = []
    cons = []
    # load table name & column name
    for table in input['Tables']:
        tb_name = table['Table Name']
        tb_col_distribution = table['Column Distribution']
        tb_cols = []
        for col in table['Table Columns']:
            col_name = col['Column Name']
            col_type = col['Data Type']
            tb_cols.append(key(col_name,col_type))
        
        prim_key = key(table['Primary Key']['Name'],table['Primary Key']['Data Type'])
        for con in table['Foreign Key']:
            foreign_cons.append(foreign_constraint(tb_name,key(con['Foreign Key Name'],con['Foreign Key Type']),
                                                con['Referenced Table'],key(con['Referenced Primary Key'],con['Referenced Primary Key Type'])))
        all_tables.append(Table(tb_name,tb_cols,prim_key,foreign_cons,tb_col_distribution))
    # load constraints
    for con in input['Constraints']:
        cons.append(input['Constraints'][con])
    # print(cons)
    fea = feature(cons[0],cons[1],cons[2],cons[3],cons[4],cons[5],cons[6],cons[7],cons[8],cons[9],cons[10])
    #print(cons[0],cons[1],cons[2],cons[3],cons[4])
    dbs=DBschema(tbs=all_tables,foreign_constraint=foreign_cons)
    outputFile=input['Generation File']
    return dbs,fea,outputFile

# cons应该是feature类型
# fea=feature(cons[0],cons[1])
# return DBschema,feature

class SQLGen:
    def __init__(self,dbs) -> None:
        self.sql_set=[]
        self.last_sql=simpleSQL()
        self.dbs=dbs

    def generate(self,condition):
        # feature1 : read/write ratio
        rw_choice=rand_num_sampling(0,1,np.array([condition.rwRatio,1-condition.rwRatio]))
        # feature2 : average table num
        tb_num=rand_num_sampling(1,2,condition.averageTableNum)
        # feature3 : table data distribution
        # tb_choice=self.dbs.tables[randNumGen(0,len(self.dbs.tables)-1,[1.0/len(self.dbs.tables) for i in range(len(self.dbs.tables))])]
        # print('aaaa')
        tb_choice=self.dbs.tables[rand_num_sampling(0,len(self.dbs.tables)-1,condition.tableDistribution)]
        # feature4 : different query comparison constraint ratio
        # cons=randNumGen(0,3,[1.0/4 for i in range(4)])
        cons=rand_num_sampling(0,3,condition.queryComparisonOperatorRatio)
        # feature5 : query data domain distribution
        data=rand_num_sampling(0,99,[1.0/100 for i in range(100)])
        if rw_choice==0:
            self.last_sql.add(key(value="select",type="keyword"))
            self.last_sql.add(key(value="*",type="colname"))
            self.last_sql.add(key(value="from",type="keyword"))
            self.last_sql.add(key(value=tb_choice.name,type="tbname"))
            self.last_sql.add(key(value="where",type="keyword"))
            self.last_sql.add(key(value=tb_choice.col[0].value,type="colname"))
            if cons==0:
                self.last_sql.add(key(value=">",type="compare"))
            else:
                if cons==1:
                    self.last_sql.add(key(value="<",type="compare"))
                else:
                    if cons==2:
                        self.last_sql.add(key(value="=",type="compare"))
                    else: 
                        if cons==3:
                            self.last_sql.add(key(value="!=",type="compare"))
                        else: 
                            pass
            self.last_sql.add(key(value=data,type="value"))
            self.last_sql.add(key(value=";",type="end"))
        else:
            self.last_sql.add(key(value="insert",type="keyword"))
            self.last_sql.add(key(value="into",type="keyword"))
            self.last_sql.add(key(value=tb_choice.name,type="tbname"))
            self.last_sql.add(key(value="value",type="keyword"))
            tmp="("
            for i in range(len(tb_choice.col)):
                if i!=0:
                    tmp+=","
                tmp+=str(rand_num_sampling(0,99,[1.0/100 for i in range(100)]));
            tmp+=")"
            self.last_sql.add(key(value=tmp,type="value"))
            self.last_sql.add(key(value=";",type="end"))
        
        self.sql_set.append(self.last_sql)
        return self.last_sql

    def save(self,outputFile):
        with open(outputFile, 'w') as f:
            for it in self.sql_set:
                f.write(it.toStr())
        print(f"workload saved to {outputFile}")