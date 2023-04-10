from base import *
import argparse

def getNTable(dbs,n,pdg):
    # print(n)
    all_tb=[dbs.tables[i] for i in range(len(dbs.tables))]
    # all_tb=[i for i in len(dbs.tables)]
    tb_set=set()
    tb_selected = []
    tb_sub_distribution = []
    if len(all_tb)<n:
        print("fatal error : dbs table num not enough.")
        return -1,set()
    # possibly sample to the same table
    while len(tb_set)<n:
        x=rand_num_sampling(0,len(all_tb)-1,pdg)
        if x!=-1:
            tb_set.add(dbs.tables[x])
            if dbs.tables[x] not in tb_selected:
                tb_selected.append(dbs.tables[x])
                tb_sub_distribution.append(table2dist[dbs.tables[x]])
            else:
                continue
            # print(str(len(tb_set))+"add"+str(fea.tableDistribution[x]))
        else:
            return -1,set()
    # make tb_sub_distribution sum to 1
    sum_of_tsd = 0
    for i in tb_sub_distribution:
        sum_of_tsd = sum_of_tsd + i
    # print(tb_sub_distribution)
    for i in range(len(tb_sub_distribution)):
        tb_sub_distribution[i] = tb_sub_distribution[i]/sum_of_tsd
    # print(tb_sub_distribution)
    return 1,tb_set,tb_sub_distribution

def get1Table(tbs,pdg):
    # print("get1"+str(len(tbs)-1))
    return dbs.tables[rand_num_sampling(0,len(tbs)-1,pdg)]

def get1Column(tb,pdg):
    return tb.col[rand_num_sampling(0,len(tb.col)-1,pdg)]

def from_tb_get_continuous_type_column(tbs):
    pass
    
def from_tb_get_discrete_type_column(tbs):
    pass

def from_tb_get_N_columns_for_aggregation(tbs,aggregationNum):
    
    col_set=set()
    while(len(col_set)<aggregationNum):
        tb_choice=tbs[rand_num_sampling(0,len(tbs)-1,np.full(len(tbs),1.0/len(tbs)))]
        col_choice=get1Column(tb_choice,np.full(len(tb_choice.col),1.0/len(tb_choice.col)))
        col_set.add(key(value=col_choice,type=tb_choice))
        # pass
    return list(col_set)

class SQLGen2(SQLGen):
    def generate(self,condition):
        self.last_sql=simpleSQL()
        rw_choice=rand_num_sampling(0,1,np.array([condition.rwRatio,1-condition.rwRatio]))
        if rw_choice==0:
            # read
            tb_num=rand_num_sampling(1,2,condition.averageTableNum)
            
            if tb_num==1:
                tb_choice=get1Table(self.dbs.tables,condition.tableDistribution)
                col_choice=get1Column(tb_choice,tb_choice.column_distribution)
                
                self.last_sql.add(key(value="select",type="keyword"))
                
                on=rand_num_sampling(0,2,condition.averageAggregationOperatorNum)
                aqcn=min(len(tb_choice.col),len(condition.averageQueryColomnNum)-1)
                qcn=rand_num_sampling(0,aqcn,[1.0/(aqcn+1) for i in range(aqcn+1)])
                
                if qcn==0:
                    self.last_sql.add(key(value="*",type="colname"))
                else:
                    if col_choice.type=='varchar':
                        aggregation_type=0
                    else:
                        aggregation_type=rand_num_sampling(1,3,[1.0/3 for i in range(3)])
                        
                    if aggregation_type==0:
                        tmp=f'count({col_choice.value}) as count_value_{col_choice.value}'
                    elif aggregation_type==1:
                        tmp=f'avg({col_choice.value}) as average_value_{col_choice.value}'
                    elif aggregation_type==2:
                        tmp=f'min({col_choice.value}) as minimum_value_{col_choice.value}'
                    elif aggregation_type==3:
                        tmp=f'max({col_choice.value}) as maximum_value_{col_choice.value}'
                                
                    self.last_sql.add(key(value=tmp,type="aggregation"))
                    
                self.last_sql.add(key(value="from",type="keyword"))
                self.last_sql.add(key(value=tb_choice.name,type="tbname"))
                
                hasGroupBy=rand_num_sampling(0,1,condition.groupByRatio)
                # print("groupby")
                tb_choice=get1Table(self.dbs.tables,condition.tableDistribution)
                col_choice=get1Column(tb_choice,tb_choice.column_distribution)
                
                if hasGroupBy==0 or col_choice.type!="varchar":
                    
                    self.last_sql.add(key(value="where",type="keyword"))
                    
                    qc_num=rand_num_sampling(1,3,condition.queryLogicPredicateNum)
                    for i in range(qc_num):
                        if i!=0:
                            if rand_num_sampling(0,1,[0.5,0.5])==0:
                                self.last_sql.add(key(value="and",type="predicate"))
                            else:
                                self.last_sql.add(key(value="or",type="predicate"))
                        
                        # tb_choice=get1Table(self.dbs,np.full(len(self.dbs.tables),1.0/len(self.dbs.tables)))
                        # col_choice=get1Column(tb_choice,np.full(len(tb_choice.col),1.0/len(tb_choice.col)))
                        col_choice=get1Column(tb_choice,tb_choice.column_distribution)

                        self.last_sql.add(key(value=tb_choice.name,type="tbname_"))
                        self.last_sql.add(key(value=".",type="dot"))
                        self.last_sql.add(key(value=col_choice.value,type="colname"))
                        
                        cons=rand_num_sampling(0,3,condition.queryComparisonOperatorRatio)
                        if cons==0:
                            self.last_sql.add(key(value=">",type="compare"))
                        elif cons==1:
                            self.last_sql.add(key(value="<",type="compare"))
                        elif cons==2:
                            self.last_sql.add(key(value="=",type="compare"))
                        elif cons==3:
                            self.last_sql.add(key(value="!=",type="compare"))
                        else:
                            pass
                        data=rand_num_sampling(0,99,[1.0/100 for i in range(100)])
                        self.last_sql.add(key(value=data,type="value"))
                    
                    # self.sql.add(key(value=";",type="end"))
                else:
                    self.last_sql.add(key(value="group by",type="keyword"))
                    self.last_sql.add(key(value=col_choice.value,type="colname"))
                
                hasOrderBy=rand_num_sampling(0,1,condition.descOrAsc)
                descOrAsc=rand_num_sampling(0,1,[0.5,0.5])
                col_choice=get1Column(tb_choice,tb_choice.column_distribution)
                if hasOrderBy==1 and col_choice.type!="varchar" and descOrAsc==0:
                    self.last_sql.add(key(value="order by",type="keyword"))
                    self.last_sql.add(key(value=col_choice.value,type="colname"))
                    self.last_sql.add(key(value="desc",type="sort"))
                elif hasOrderBy==1 and col_choice.type!="varchar":
                    self.last_sql.add(key(value="order by",type="keyword"))
                    self.last_sql.add(key(value=col_choice.value,type="colname"))
                    self.last_sql.add(key(value="asc",type="sort"))
                else:
                    pass
                
            elif tb_num==2:
                # JOIN
                bool,tbs,tbs_sub_distribution=getNTable(dbs=dbs,n=2,pdg=np.full(len(dbs.tables),1.0/len(dbs.tables)))
                tbs_=list(tbs)
                if bool==-1:
                    print("fatal error : dbs sampled failed.")
                else:
                    self.last_sql.add(key(value="select",type="keyword"))
                    
                    on=rand_num_sampling(0,2,condition.averageAggregationOperatorNum)
                    aqcn=len(condition.averageQueryColomnNum)-1
                    qcn=rand_num_sampling(0,aqcn,[1.0/(aqcn+1) for i in range(aqcn+1)])
                    
                    if qcn==0:
                        self.last_sql.add(key(value="*",type="colname"))
                    else:
                        res=from_tb_get_N_columns_for_aggregation(tbs_,qcn)
                        n_col=[res[i].value for i in range(len(res))]
                        n_col_from_tb=[res[i].type for i in range(len(res))]
                        for i,col in enumerate(n_col):
                            if i<on:
                                if col.type=='varchar':
                                    aggregation_type=0
                                else:
                                    aggregation_type=rand_num_sampling(1,3,[1.0/3 for i in range(3)])  
                                if aggregation_type==0:
                                    tmp=f'count({n_col_from_tb[i].name}.{col.value}) as count_value_{col.value}'
                                elif aggregation_type==1:
                                    tmp=f'avg({n_col_from_tb[i].name}.{col.value}) as average_value_{col.value}'
                                elif aggregation_type==2:
                                    tmp=f'min({n_col_from_tb[i].name}.{col.value}) as minimum_value_{col.value}'
                                elif aggregation_type==3:
                                    tmp=f'max({n_col_from_tb[i].name}.{col.value}) as maximum_value_{col.value}'
                                
                                if i!=qcn-1:
                                    self.last_sql.add(key(value=tmp,type="colname_"))
                                else:
                                    self.last_sql.add(key(value=tmp,type="colname"))
                                
                            else:
                                if i!=qcn-1:
                                    self.last_sql.add(key(value=f"{n_col_from_tb[i].name}.{col.value}",type="colname_"))
                                else:
                                    self.last_sql.add(key(value=f"{n_col_from_tb[i].name}.{col.value}",type="colname"))
                            # print(i.value)
                            if i!=qcn-1:
                                self.last_sql.add(key(value=",",type="dot"))

                    self.last_sql.add(key(value="from",type="keyword"))

                    self.last_sql.add(key(value=tbs_[0].name,type="tbname"))
                    self.last_sql.add(key(value="join",type="keyword"))
                    self.last_sql.add(key(value=tbs_[1].name,type="tbname"))
                    self.last_sql.add(key(value="where",type="keyword"))
                    
                    self.last_sql.add(key(value=tbs_[0].name,type="tbname_"))
                    self.last_sql.add(key(value=".",type="dot"))
                    self.last_sql.add(key(value=tbs_[0].col[0].value,type="colname"))
                    
                    self.last_sql.add(key(value="=",type="compare"))
                    
                    self.last_sql.add(key(value=tbs_[1].name,type="tbname_"))
                    self.last_sql.add(key(value=".",type="dot"))
                    self.last_sql.add(key(value=tbs_[1].col[0].value,type="colname"))
                    
                    qc_num=rand_num_sampling(1,3,condition.queryLogicPredicateNum)
                    if qc_num>1:
                        
                        for i in range(qc_num-1):
                            if rand_num_sampling(0,1,[0.5,0.5])==0:
                                self.last_sql.add(key(value="and",type="predicate"))
                            else:
                                self.last_sql.add(key(value="or",type="predicate"))
                            
                            tb_choice=get1Table(tbs_,tbs_sub_distribution)
                            col_choice=get1Column(tb_choice,tb_choice.column_distribution)
                            
                            self.last_sql.add(key(value=tb_choice.name,type="tbname_"))
                            self.last_sql.add(key(value=".",type="dot"))
                            self.last_sql.add(key(value=col_choice.value,type="colname"))
                        
                            cons=rand_num_sampling(0,3,condition.queryComparisonOperatorRatio)
                            if cons==0:
                                self.last_sql.add(key(value=">",type="compare"))
                            elif cons==1:
                                self.last_sql.add(key(value="<",type="compare"))
                            elif cons==2:
                                self.last_sql.add(key(value="=",type="compare"))
                            elif cons==3:
                                self.last_sql.add(key(value="!=",type="compare"))
                            else:
                                pass
                            data=rand_num_sampling(0,99,[1.0/100 for i in range(100)])
                            self.last_sql.add(key(value=data,type="value"))
                        
                            # self.sql.add(key(value=";",type="end"))
                    else:
                        pass
            else:
                pass
            
        elif rw_choice==1:
            tb_choice=self.dbs.tables[rand_num_sampling(0,len(self.dbs.tables)-1,condition.tableDistribution)]
            self.last_sql.add(key(value="insert",type="keyword"))
            self.last_sql.add(key(value="into",type="keyword"))
            self.last_sql.add(key(value=tb_choice.name,type="tbname"))
            self.last_sql.add(key(value="value",type="keyword"))
            tmp="("
            for i in range(len(tb_choice.col)):
                if i!=0:
                    tmp+=","
                if tb_choice.col[i].type=='varchar':
                    tmp+=rand_str_sampling(5)
                else:
                    tmp+=str(rand_num_sampling(0,99,[1.0/100 for i in range(100)]));
            tmp+=")"
            self.last_sql.add(key(value=tmp,type="value"))
            # self.sql.add(key(value=";",type="end"))
        else:
            pass
        self.sql_set.append(self.last_sql)
        return self.last_sql

    def generate_N(self, condition, outputFile):
        self.sql_set=[]
        # ans=list()
        for i in range(condition.workloadSize):
            self.generate(condition)
        
        if condition.workloadSize==len(self.sql_set):
            print("workload generation succeeded.")
            self.save(outputFile)
        else:
            print("fatal error : generation failed. Please check your schema input.")
            return

if __name__=='__main__':
    # python workloadGen.py --config_file ./input.json
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_file', type=str, default='./input.json')
    
    args = parser.parse_args()
    
    all_tables,fea,outputFile=load_json(args.config_file,'r')
    table2dist = {}
    for i in range(len(all_tables.tables)):
        table2dist[all_tables.tables[i]] = fea.tableDistribution[i]
    dbs=all_tables
    sg=SQLGen2(dbs=dbs)
    # sg.generate(condition=fea)
    # print(sg.last_sql.toStr())
    sg.generate_N(condition=fea,outputFile=outputFile)
    