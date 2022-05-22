def info(msg: str):
    print('\033[1;32;40m[INFO]\033[0;37;40m', msg)


def warn(msg: str):
    print('\033[1;33;40m[WARN]\033[0;37;40m', msg)    


def error(msg: str):
    print('\033[1;31;40m[ERROR]\033[0;37;40m', msg)  