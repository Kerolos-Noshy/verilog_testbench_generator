import tkinter as tk
import hdlparse.verilog_parser as vlog
import re
import random

window = tk.Tk()
window.geometry("500x400")
window.resizable(width=False, height=False)
window.title('Testbench generator')
l1 = tk.Label(window, text="Verilog testbench generator", font=("Arial", 18), fg="black")

path = tk.Label(window, text="Enter verilog file path: ", font=(12))
e1 = tk.Entry(window, width=40)
l3 = tk.Label(window, text="Enter time delay ", font=(12))
e2 = tk.Entry(window, width=5)
l2 = tk.Label(window, text="File generated successfully at the same path", font=(12), fg='green')
l4 = tk.Label(window, text="Error, please enter valid path and time", font=(12), fg='red')


def message(flag):
    if flag == 0:
        l4.place(x=80,y=270)
        l2.place(x=500, y=500)
    else:
        l2.place(x=60, y=270)
        l4.place(x=500,y=500)


def get_data(flag):
    data = [e1.get(), e2.get()]
    message(flag)
    return data


l1.place(x=80, y=10)
l2.place(x=500, y=500)
path.place(x=160, y=90)
e1.place(x=100, y=120)
l3.place(x=180, y=150)
e2.place(x=230, y=180)


def start():
    vlog_ex = vlog.VerilogExtractor()
    global fname
    global time_delay
    try:
        flag = False
        fname = get_data(flag)[0]
        with open(fname, 'rt') as fh:
            code = fh.read()

    except FileNotFoundError:
        flag = False
        get_data(flag)
    try:
        time_delay = int(get_data(flag)[1])
    except ValueError:
        flag = False
        get_data(flag)
    # vlog_mods = vlog_ex.extract_objects_from_source(code)
    vlog_mods = vlog_ex.extract_objects(fname)


    def vector_size(line):
        if re.search(r'\[', line):
            lval = re.findall(r'\[(.*):', line)[0]
            rval = re.findall(r'\[.*:(.*)\]', line)[0]
            return (abs(int(rval) - int(lval)) + 1)
        return 1

    for m in vlog_mods:
        inputs_list = []
        for p in m.ports:
            if (p.data_type).find('[') != -1:
                inputs_list.append({"name": p.name, "mode": p.mode, "data_type": (p.data_type).split()[0],
                                    "length": vector_size((p.data_type).split()[1])})
            else:
                inputs_list.append({"name": p.name, "mode": p.mode, "data_type": p.data_type, "length": 1})

    def generate_vector(port_length):
        if port_length == 1:
            return ' '
        else:
            return (' [' + str(port_length - 1) + ':0] ')

    def generate_range(port_length):
        if port_length == 1:
            return '1'
        else:
            return str(pow(2, port_length) - 1)

    def testbench_header_and_ports():
        content = ""
        content += ('module ' + m.name + '_tb();\n')
        for port in inputs_list:
            if port["mode"].find('input', 0, 5) != -1:
                content += ('    ' + port["mode"].replace('input', 'reg') + generate_vector(port["length"]) + port[
                    "name"] + '_tb;\n')
            elif port["mode"].find('output', 0, 6) != -1:
                content += ('    ' + port["mode"].replace('output', 'wire') + generate_vector(port["length"]) + port[
                    "name"] + '_tb;\n')
        return content

    def testbench_initial_block(time_delay):
        global val
        content = ""
        content += ('  integer i;\n  begin\n//initial block\ninitial\n  begin\n    //initial values\n')
        minPortSize = 20
        for port in inputs_list:
            minPortSize = max(port["length"], minPortSize)
        iterationCounter = int(pow(2, minPortSize) / 2)
        iterationCounter = min(iterationCounter, 30)
        for i in range(iterationCounter):
            if (i != 0):
                content += ('  #' + str(time_delay) + '\n')
            for line in inputs_list:
                if line["mode"] == 'input':
                    val = line["length"]
                    content += ('    ' + line["name"] + '_tb = ' + str(val) + '\'b' + bin(
                        random.randint(0, pow(2, val) - 1))[2:].zfill(val) + ';' + '\n')

        content += ('\n//Random generated constraints\n')
        content += ('for(i = 0; i < 100; i = i+1)\n  begin\n  #' + str(time_delay) + '\n')
        for line in inputs_list:
            if line["mode"] == 'input':
                val = line["length"]
                content += ('    ' + line["name"] + '_tb = ' + '$urandom_range(0,' + generate_range(val) + ');' + '\n')
        content += ('  end\n')
        content += ('  $finish;\nend\n')
        return content

    def testbench_design_instance():
        content = ""
        content += ('// instaniate design instance\n  ' + m.name + ' DUT (\n')
        for i, line in enumerate(inputs_list, 0):
            content += ('    .' + (line["name"]).replace('_tb', '') + '(' + line["name"] + '_tb' + ')')
            if i != len(inputs_list) - 1:
                content += (',\n')
            else:
                content += ('\n);\n')
        return content

    def testbench_monitor_block():
        content = ""
        word_size = []
        content += ('initial begin\n  $display ("        			","Time ')
        for port in inputs_list:
            content += (port["name"] + '  ')
            word_size.append(len(port["name"]))
        content += ('");\n  $monitor("     %d')
        for i in range(1, len(inputs_list) + 1):
            w = max(word_size[i - 1], port["length"])
            content += ('{space:{width}}{id}'.format(space=' ', width=w, id='%d'))
        content += ('" , $time')
        for port in inputs_list:
            content += (',' + port["name"] + '_tb')
        content += (');\nend\nend\nendmodule')
        return content

    def generate_output_file(file_content):
        global flag
        output_file = fname.replace('.v', '_tb.v')
        with open(output_file, 'w') as f:
            f.write(file_content)
            flag = True
            get_data(flag)

    test_bench_content = ""
    test_bench_content += testbench_header_and_ports() + testbench_initial_block(
        time_delay) + testbench_design_instance() + testbench_monitor_block()

    generate_output_file(test_bench_content)


b1 = tk.Button(window, text="Generate", font=(13), command=start)
b1.place(x=200, y=220)

if __name__ == '__main__':
    window.mainloop()
