import requests
import os
from pathlib import Path
import time
from datetime import datetime
from calculations import cpu, ram, calculate
name = "a349"
home = Path.home()
path = os.path.join(home, 'computer.txt')
print(path)

def create_computer(name):
    data = requests.post(f"http://localhost:3000/computer/?name={name}")
    return data.json()

def get_computer_id(path):
    with open(path, 'r') as input_file:
        f = input_file.readlines()
        id = f[0]
        return id

if not os.path.exists(path):
    data = create_computer(name)
    id_file = open(path, "w")
    id_file.write(str(data['id']))

time_start = time.time()
curr_time = time.time()
period = float(input())
computer_id = get_computer_id(path)
print(computer_id)
st_cpu_con, st_ram_con = 0, 0
while curr_time - time_start < period:
    ttime = datetime.now()
    cpu_con, ram_con, total_con, co2, price, st_cpu_con, st_ram_con = calculate(cpu, ram, st_cpu_con, st_ram_con)
    data = {'comp_id':computer_id, 'time':ttime, 'cpu_consumption': cpu_con, 'ram_consumption':ram_con,
            'total_consumption':total_con, 'co2': co2, 'price': price}
    requests.post(f"http://localhost:3000/consumption/?comp_id={computer_id}", data=data)
    curr_time = time.time()
