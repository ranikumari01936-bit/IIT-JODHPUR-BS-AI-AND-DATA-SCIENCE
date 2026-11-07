"""
file_manager.py
Opens, reads and closes a dataset file, storing its content in a variable.
"""

FILE_NAME = "data.txt"

# ---------------------------------------------------------------
# Method 1: explicit open() -> read() -> close()
# ---------------------------------------------------------------
file_handle = open(FILE_NAME, "r")       # OPEN in read mode ("r")
try:
    file_content = file_handle.read()    # READ: disk -> main memory variable
finally:
    file_handle.close()                  # CLOSE: always release the file
print("File closed (Method 1):", file_handle.closed)

# ---------------------------------------------------------------
# Method 2: 'with' statement (closes the file automatically)
# ---------------------------------------------------------------
with open(FILE_NAME, "r") as f:          # OPEN in read mode ("r")
    data = f.read()                      # READ into variable 'data'
print("File closed (Method 2):", f.closed)   # True -> auto-closed by 'with'

# ---------------------------------------------------------------
# Output: content now lives in memory variables, not on disk
# ---------------------------------------------------------------
print("\n===== Content of", FILE_NAME, "(stored in variable) =====")
print(data)
lines = data.splitlines()
print("Total lines read :", len(lines))
print("Header           :", lines[0])
for row in lines[1:]:
    print("Data row         :", row)
