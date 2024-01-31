import psutil
import cpuinfo



def get_system_info():
    cpu_info = {
        "name": f"{cpuinfo.get_cpu_info()['brand_raw']}",
        "load_percent": psutil.cpu_percent(),
        "cores": cpuinfo.get_cpu_info()['count']
    }

    mem_info = {
        "total_ram": f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB",
        "used_ram": f"{round(psutil.virtual_memory().used / (1024 ** 3), 2)} GB",
        "ram_percent": psutil.virtual_memory().percent
    }

    disk_info = {
        "total_disk": f"{round(psutil.disk_usage('/').total / (1024 ** 3), 2)} GB",
        "used_disk": f"{round(psutil.disk_usage('/').used / (1024 ** 3), 2)} GB",
        "disk_percent": psutil.disk_usage('/').percent
    }

    return cpu_info, mem_info, disk_info
