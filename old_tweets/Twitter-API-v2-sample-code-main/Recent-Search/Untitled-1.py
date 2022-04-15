#%%
# import findspark
# findspark.init(r'C:\spark-3.2.0-bin-hadoop3.2')
# findspark.find()
from pyspark import SparkConf, SparkContext

# Obtain entry point into Spark
conf = SparkConf().setMaster("local").setAppName("AutoPostSales")
sc = SparkContext(conf=conf)
# %%
# import pyspark 
# from pyspark import sql
# from pyspark.sql import SparkSession
from pyspark import SparkContext
# conf = pyspark.SparkConf().setAppName('SparkApp').setMaster("local")
# spark = sql.SparkSession \
#     .builder \
#     .appName("SparkApp").getOrCreate()
    # .config("spark.some.config.option", "some-value") \
sc = SparkContext('local[*]')
# %%
numeric_val = sc.parallelize([1,2,3,4])
numeric_val.map(lambda x: x*x*x).collect()

# %%
sc.stop()
# %%
