from timeit import default_timer as timer
import parser


# Usage:
# 1) Clear DB with command:  python db.py 0
# 1) Launch script:  python benchmark.py
if __name__ == '__main__':
    start = timer()
    parser.parse('csv')
    # parser.parse('xml')
    end = timer()
    print(end - start)