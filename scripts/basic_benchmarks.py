import os

path = "/mnt/pmem0/kvdk"
report_path = "./results/"
value_sizes = [120]
data_size = 100 * 1024 * 1024 * 1024
instance_space = 384 * 1024 * 1024 * 1024  # we need enough space to test insert
benchmark_threads = 48
kvdk_max_write_threads = 48
duration = 10
populate = 1

numanode = 0
bin = "../build/bench"
exec = "numactl --cpunodebind={0} --membind={0} {1}".format(numanode, bin)


def Confirm(dir):
    y = input("Instance path : {}, it will be removed and recreated, confirm? (y/n)".format(dir))
    if y != 'y':
        exit(1)


if __name__ == "__main__":
    Confirm(path)
    os.system("mkdir -p {}".format(report_path))
    for vs in value_sizes:
        num = data_size // (vs + 8)
        para = "-populate={} -value_size={} -threads={} -time={} -path={} -num={} -space={} -max_write_threads={}".format(
            populate,
            vs,
            benchmark_threads,
            duration,
            path, num,
            instance_space,
            kvdk_max_write_threads)
        # Benchmark string-type data
        # fill uniform distributed kv
        os.system("rm -rf {0}".format(path))
        new_para = para + " -fill=1 -type=string"
        report = report_path + "string_vs{}_fill_thread{}".format(vs, benchmark_threads)
        print("Fill string-type kv")
        print("{0} {1} > {2}".format(exec, new_para, report))
        os.system("{0} {1} > {2}".format(exec, new_para, report))
        # read
        new_para = para + " -fill=0 -type=string -read_ratio=1"
        report = report_path + "string_vs{}_read_thread{}".format(vs, benchmark_threads)
        print("Read string-type kv")
        os.system("{0} {1} > {2}".format(exec, new_para, report))
        # insert new kv
        new_para = para + " -fill=0 -type=string -read_ratio=0 -existing_keys_ratio=0"
        report = report_path + "string_vs{}_insert_thread{}".format(vs, benchmark_threads)
        print("Insert new string-type kv")
        os.system("{0} {1} > {2}".format(exec, new_para, report))
        # batch insert
        new_para = para + " -fill=0 -type=string -read_ratio=0 -batch=100 -existing_keys_ratio=0"
        report = report_path + "string_vs{}_batch_insert_thread{}".format(vs, benchmark_threads)
        print("Batch write string-type kv")
        os.system("{0} {1} > {2}".format(exec, new_para, report))
        # update
        new_para = para + " -fill=0 -type=string -read_ratio=0"
        report = report_path + "string_vs{}_update_thread{}".format(vs, benchmark_threads)
        print("Update string-type kv")
        os.system("{0} {1} > {2}".format(exec, new_para, report))
        # read + update
        new_para = para + " -fill=0 -type=string -read_ratio=0.9"
        report = report_path + "string_vs{}_ru91_thread{}".format(vs, benchmark_threads)
        print("Mixed read/update string-type kv")
        os.system("{0} {1} > {2}".format(exec, new_para, report))

        # Benchmark sorted-type data
        # fill uniform distributed kv
        os.system("rm -rf {0}".format(path))
        new_para = para + " -fill=1 -type=sorted"
        report = report_path + "sorted_vs{}_fill_thread{}".format(vs, benchmark_threads)
        print("Fill sorted-type kv")
        os.system("{0} {1} > {2}".format(exec, new_para, report))
        # read
        new_para = para + " -fill=0 -type=sorted -read_ratio=1"
        report = report_path + "sorted_vs{}_read_thread{}".format(vs, benchmark_threads)
        print("Read sorted-type kv")
        os.system("{0} {1} > {2}".format(exec, new_para, report))
        # insert new kvs
        new_para = para + " -fill=0 -type=sorted -read_ratio=0 -existing_keys_ratio=0"
        report = report_path + "sorted_vs{}_insert_thread{}".format(vs, benchmark_threads)
        print("Insert new sorted-type kv")
        os.system("{0} {1} > {2}".format(exec, new_para, report))
        # update
        new_para = para + " -fill=0 -type=sorted -read_ratio=0"
        report = report_path + "sorted_vs{}_update_thread{}".format(vs, benchmark_threads)
        print("Update sorted-type kv")
        os.system("{0} {1} > {2}".format(exec, new_para, report))
        # range scan
        new_para = para + " -fill=0 -type=sorted -read_ratio=1 -scan=1"
        report = report_path + "sorted_vs{}_scan_thread{}".format(vs, benchmark_threads)
        print("Scan sorted-type kv")
        os.system("{0} {1} > {2}".format(exec, new_para, report))
        # read + update
        new_para = para + " -fill=0 -type=sorted -read_ratio=0.9 -existing_keys_ratio=0"
        report = report_path + "sorted_vs{}_ru91_thread{}".format(vs, benchmark_threads)
        print("Mixed read/update sorted-type kv")
        os.system("{0} {1} > {2}".format(exec, new_para, report))
