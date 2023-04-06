## zzGen
> ### 🔧 a simple SQL query generation tool.
> ### ‘zz’ is the initial pinyin letter of the Chinese word “智障”.



## Benchbase Quickstart

In the `benchbase` folder, we have a tgz file, which can be extracted,

```bash
cd benchbase
tar xvzf benchbase-postgres.tgz
cd benchbase-postgres
```

Inside this folder, you can run BenchBase. For example, to execute the `tpcc` benchmark,

```bash
java -jar benchbase.jar -b tpcc -c config/postgres/sample_tpcc_config.xml --create=true --load=true --execute=true
```

**We modified the benchbase source code to output all the queries in the workload in text format when testing**. (Only seats, sibench, smallbank, tatp, tpcc, tpch are supported.)For example, after executing the `tpcc` benchmark, a  `tpcc_workload.txt` will be generated, each line is a query. 

A full list of options can be displayed,

```bash
java -jar benchbase.jar -h
```

