def write_to_file(filename, msg):
    with open(filename, "a") as f:
        f.write(msg + "\n")
