from controler import execute
import sys

if len(sys.argv) != 3:
    print("Usage: port database_name")
    exit(0)

cmd = "controller&show&%s" % sys.argv[2]

execute(int(sys.argv[1]), cmd)    


