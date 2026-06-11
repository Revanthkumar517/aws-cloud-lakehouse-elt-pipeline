import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col, current_timestamp, round as spark_round


args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "S3_BUCKET",
        "RAW_PREFIX",
        "CURATED_PREFIX",
    ],
)

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

job = Job(glue_context)
job.init(args["JOB_NAME"], args)

bucket = args["S3_BUCKET"]
raw_prefix = args["RAW_PREFIX"]
curated_prefix = args["CURATED_PREFIX"]

raw_base = f"s3://{bucket}/{raw_prefix}"
curated_base = f"s3://{bucket}/{curated_prefix}"


def read_csv(dataset_name):
    return (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(f"{raw_base}/{dataset_name}/")
    )


customers = read_csv("customers")
products = read_csv("products")
orders = read_csv("orders")

customers_curated = (
    customers
    .dropDuplicates(["customer_id"])
    .withColumn("ingestion_timestamp", current_timestamp())
)

products_curated = (
    products
    .dropDuplicates(["product_id"])
    .withColumn("ingestion_timestamp", current_timestamp())
)

orders_curated = (
    orders
    .dropDuplicates(["order_id"])
    .join(products.select("product_id", "unit_price"), "product_id", "left")
    .withColumn("order_amount", spark_round(col("quantity") * col("unit_price"), 2))
    .withColumn("ingestion_timestamp", current_timestamp())
)

customers_curated.write.mode("overwrite").parquet(f"{curated_base}/customers/")
products_curated.write.mode("overwrite").parquet(f"{curated_base}/products/")
orders_curated.write.mode("overwrite").partitionBy("order_status").parquet(f"{curated_base}/orders/")

job.commit()
