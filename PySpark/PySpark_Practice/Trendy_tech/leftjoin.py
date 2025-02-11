from pyspark.sql import SparkSession

# Initialize a SparkSession
spark = SparkSession.builder.appName("left_outer_join_example").getOrCreate()

# Create DataFrames for Employees and Departments
data_employees = [(1, "John", 1), (2, "Emma", 2), (3, "Raj", None), (4, "Nina", 4)]
data_departments = [(1, "HR"), (2, "Tech"), (3, "Marketing"), (None, "Temp")]

columns_employees = ["emp_id", "emp_name", "dept_id"]
columns_departments = ["dept_id", "dept_name"]

df_employees = spark.createDataFrame(data_employees, columns_employees)
df_departments = spark.createDataFrame(data_departments, columns_departments)

# Perform Left Outer Join
df_joined = df_employees.join(df_departments, df_employees.dept_id == df_departments.dept_id, "left")

# Show the result
df_joined.show()


# SELECT
#     *
# FROM
#     employees e
# LEFT JOIN
#     departments d ON e.dept_id = d.dept_id;



Table A (Employees):

emp_id	emp_name	dept_id
1	John	1
2	Emma	2
3	Raj	null
4	Nina	4
Table B (Departments):

dept_id	dept_name
1	HR
2	Tech
3	Marketing
null	Temp


Expected output:

emp_id	emp_name	dept_id	dept_id	dept_name
1	John	1	1	HR
2	Emma	2	2	Tech
3	Raj	null	null	null
4	Nina	4	null	null


|emp_id|emp_name|dept_id|dept_id|dept_name|
+------+--------+-------+-------+---------+
|     1|    John|      1|      1|       HR|
|     2|    Emma|      2|      2|     Tech|
|     3|     Raj|   null|   null|     null|  -> null values for non-matching rows
|     4|    Nina|      4|   null|     null|  -> dep_id=4 doesn't exist in departments table, thus null values for right table columns
+------+--------+-------+-------+---------+


Handling Null Values In Left Outer Join
As you've seen in the example, null dept_id doesn't match null in the right DataFrame (df_departments). Therefore, those rows are not matched and null values are used to fill in the columns from the right DataFrame.