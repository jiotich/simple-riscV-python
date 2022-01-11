import sys, time, os

insts = {"i":("addi","andi","ori"),"r":("add","sub","and","or","xor","sll","srl")}
i_funct3 = {'addi':'000','andi':'111','ori':'110'}
r_funct3 = {'add':'000','sub':'000','and':'111','or':'110','xor':'100','sll':'001','srl':'101'}

def processLine(line, debug=False, extended=False):
	if line == "":
		return
	spacing = ""
	if debug:
		spacing = " "
	inst = ""
	full = []
	res = ""
	for digit in line:
		if digit != " " and digit != ",":
			inst += digit
		elif inst:
			full.append(inst)
			inst = ""
	full.append(inst)

	if debug and extended:
		print(full)
	
	#caso I
	if full[0] in insts["i"]:
		res += twoComp(full[-1]) + spacing
		res+=reg(full[2]) + spacing
		res+= i_funct3[full[0]] + spacing
		res+=reg(full[1]) + spacing
		res+='0010011'

	#caso R
	else:
		if full[0] == 'sub':
			res+="0100000" + spacing
		else:
			res+="0000000" + spacing
		res+=reg(full[3]) + spacing
		res+=reg(full[2]) + spacing
		res+=r_funct3[full[0]] + spacing
		res+=reg(full[1]) + spacing
		res+='0110011'
	if "-f" in sys.argv:
		with open(sys.argv[3],"a") as file:
			file.write(res+"\n")
	else:
		print(res)

def twoComp(number,bits=12):
	number = int(number)
	if number < 0:
		return bin((1 << bits) + number)[2:]
	else:
		number = bin(number)[2:]
	c = bits
	for i in number:
		c-=1
	return c*'0'+str(number)

def reg(reg):
	reg = int(reg.strip('x'))
	c = 5
	for i in range(len(bin(reg)[2:])):
		c-=1
	return c*'0'+bin(reg)[2:]

def main():
	if len(sys.argv) >= 4:
		if os.path.isfile(sys.argv[3]):
			os.remove(sys.argv[3])
	with open(sys.argv[1],"r") as file:
		alli = file.readlines()
		if "-de" in sys.argv[-1]:
			for line in alli:
				processLine(line.strip("\n"),True,True)
			return
		if "-d" in sys.argv[-1]:
			for line in alli:
				processLine(line.strip("\n"),True)
			return
		for line in alli:
			processLine(line.strip("\n"))
start = time.time()
main()
print("\nexecutado em: %s s" % (time.time()-start))