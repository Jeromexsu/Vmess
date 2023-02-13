with open("../conf/JMess_ClashX_template.yaml","r") as temp:
    lines = temp.readlines()
    for (index,line) in enumerate(lines):
        if line == '    uuid:\n':
            lines[index] = line[:-1]+" fsfdfsfdsfd\n"
with open("../conf/JMess_ClashX.yaml",'w') as conf:
    for line in lines: conf.write(line)

