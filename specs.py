# -*- coding: utf-8 -*-

import platform
import psutil
import cpuinfo
import wmi
import datetime
import re
import json
import sys
import questionary # Импортируем questionary

def get_size(bytes_val, suffix="B"):
    """Масштабирует байты в удобный для чтения формат (КБ, МБ, ГБ)."""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes_val < factor:
            return f"{bytes_val:.2f}{unit}{suffix}"
        bytes_val /= factor

def get_gpu_vendor(pnp_device_id):
    """
    Пытается определить вендора видеокарты (MSI, Asus, и т.д.)
    по Subsystem Vendor ID из строки PNPDeviceID.
    """
    vendor_map = {
        "1043": "ASUS",
        "1458": "Gigabyte",
        "1462": "MSI (Micro-Star International)",
        "19DA": "Zotac",
        "1B4C": "KFA2 / GALAX",
        "1569": "Palit",
        "1682": "XFX",
        "1DA2": "Sapphire",
        "1F0A": "PowerColor",
        "3842": "EVGA",
        "10DE": "NVIDIA (Founders Edition)",
        "1002": "AMD (Reference Card)",
    }
    
    match = re.search(r"SUBSYS_....([0-9A-F]{4})", str(pnp_device_id).upper())
    if match:
        svid = match.group(1)
        return vendor_map.get(svid, f"Неизвестный вендор (SVID: {svid})")
    
    return None

def get_cpu_info_formatted():
    """Собирает и форматирует информацию о процессоре."""
    try:
        cpu_info = cpuinfo.get_cpu_info()
        text = f"Процессор (CPU)\n"
        text += f"  - Модель: {cpu_info.get('brand_raw', 'Не удалось определить')}\n"
        text += f"  - Архитектура: {cpu_info.get('arch_string_raw', 'Не удалось определить')}\n"
        text += f"  - Физические ядра: {psutil.cpu_count(logical=False)}\n"
        text += f"  - Логические процессоры (потоки): {psutil.cpu_count(logical=True)}\n"
        return text
    except Exception as e:
        return f"Процессор (CPU)\n  - Не удалось получить информацию о CPU: {e}\n"

def get_gpu_info_formatted(wmi_instance):
    """Собирает и форматирует информацию о видеокарте."""
    text = f"Видеокарта (GPU)\n"
    try:
        gpus = wmi_instance.Win32_VideoController()
        if gpus:
            for i, gpu in enumerate(gpus, 1):
                text += f"  - Видеокарта #{i}:\n"
                vendor_name = get_gpu_vendor(gpu.PNPDeviceID)
                if vendor_name:
                    text += f"    - Производитель (Вендор): {vendor_name}\n"
                text += f"    - Модель: {gpu.Name}\n"
                if gpu.AdapterRAM:
                    text += f"    - Объем видеопамяти: {get_size(int(gpu.AdapterRAM))}\n"
                if gpu.DriverVersion:
                    text += f"    - Версия драйвера: {gpu.DriverVersion}\n"
        else:
            text += "  - Видеокарта не найдена.\n"
        return text
    except Exception as e:
        return f"Видеокарта (GPU)\n  - Не удалось получить информацию о GPU: {e}\n"

def get_ram_info_formatted(wmi_instance):
    """Собирает и форматирует информацию об оперативной памяти."""
    text = f"Оперативная память (RAM)\n"
    try:
        svmem = psutil.virtual_memory()
        text += f"  - Общий объем: {get_size(svmem.total)}\n"
        ram_modules = wmi_instance.Win32_PhysicalMemory()
        if ram_modules:
            text += "  - Установленные модули:\n"
            for i, module in enumerate(ram_modules, 1):
                text += f"    - Модуль #{i}:\n"
                text += f"      - Производитель: {module.Manufacturer or 'N/A'}\n"
                text += f"      - Объем: {get_size(int(module.Capacity))}\n"
                text += f"      - Скорость: {module.Speed or 'N/A'} MHz\n"
                text += f"      - Part Number: {module.PartNumber.strip() if module.PartNumber else 'N/A'}\n"
        return text
    except Exception as e:
        return f"Оперативная память (RAM)\n  - Не удалось получить информацию о RAM: {e}\n"

def get_board_info_formatted(wmi_instance):
    """Собирает и форматирует информацию о материнской плате."""
    text = f"Материнская плата\n"
    try:
        board = wmi_instance.Win32_BaseBoard()[0]
        text += f"  - Производитель: {board.Manufacturer}\n"
        text += f"  - Модель: {board.Product}\n"
        text += f"  - Серийный номер: {board.SerialNumber}\n"
        return text
    except IndexError:
        return "Материнская плата\n  - Не удалось получить информацию о материнской плате.\n"
    except Exception as e:
        return f"Материнская плата\n  - Не удалось получить информацию о материнской плате: {e}\n"

def get_storage_info_formatted(wmi_instance):
    """Собирает и форматирует информацию о накопителях."""
    text = f"Накопители (SSD/HDD)\n"
    try:
        disks = wmi_instance.Win32_DiskDrive()
        for i, disk in enumerate(disks, 1):
            text += f"  - Диск #{i}:\n"
            text += f"    - Модель: {disk.Model}\n"
            text += f"    - Объем: {get_size(int(disk.Size))}\n"
            text += f"    - Тип интерфейса: {disk.InterfaceType}\n"
        return text
    except Exception as e:
        return f"Накопители (SSD/HDD)\n  - Не удалось получить информацию о накопителях: {e}\n"

def get_os_info_formatted():
    """Собирает и форматирует информацию об операционной системе."""
    try:
        text = f"Операционная система\n"
        text += f"  - Система: {platform.system()} {platform.release()} ({platform.version()})\n"
        text += f"  - Разрядность: {platform.machine()}\n"
        return text
    except Exception as e:
        return f"Операционная система\n  - Не удалось получить информацию об ОС: {e}\n"

def get_system_info_text():
    """Собирает и форматирует всю информацию о системе в текстовом виде."""
    try:
        c = wmi.WMI()
        
        cpu_text = get_cpu_info_formatted()
        gpu_text = get_gpu_info_formatted(c)
        ram_text = get_ram_info_formatted(c)
        board_text = get_board_info_formatted(c)
        storage_text = get_storage_info_formatted(c)
        os_text = get_os_info_formatted()

        report = (
            f"=========================================\n"
            f"   Отчет о комплектующих компьютера\n"
            f"=========================================\n"
            f"Дата создания отчета: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n\n"
            f"{'='*20} ПРОЦЕССОР {'='*20}\n{cpu_text}\n"
            f"{'='*20} ВИДЕОКАРТА {'='*21}\n{gpu_text}\n"
            f"{'='*20} ОПЕРАТИВНАЯ ПАМЯТЬ {'='*14}\n{ram_text}\n"
            f"{'='*20} МАТЕРИНСКАЯ ПЛАТА {'='*14}\n{board_text}\n"
            f"{'='*20} НАКОПИТЕЛИ {'='*22}\n{storage_text}\n"
            f"{'='*20} ОПЕРАЦИОННАЯ СИСТЕМА {'='*11}\n{os_text}\n"
        )
        return report

    except Exception as e:
        return f"Произошла общая ошибка при сборе информации: {e}\n\nВозможно, потребуется запустить скрипт от имени Администратора для получения всех данных."

def get_system_info_json():
    """Собирает всю информацию о системе в формате JSON."""
    data = {
        "report_date": datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
        "cpu": {},
        "gpu": [],
        "ram": {},
        "motherboard": {},
        "storage": [],
        "os": {}
    }

    try:
        c = wmi.WMI()

        # CPU
        try:
            cpu_info = cpuinfo.get_cpu_info()
            data["cpu"] = {
                "model": cpu_info.get('brand_raw', 'N/A'),
                "architecture": cpu_info.get('arch_string_raw', 'N/A'),
                "physical_cores": psutil.cpu_count(logical=False),
                "logical_processors": psutil.cpu_count(logical=True)
            }
        except Exception:
            data["cpu"] = {"error": "Failed to get CPU info"}

        # GPU
        try:
            gpus = c.Win32_VideoController()
            for gpu in gpus:
                gpu_data = {
                    "model": gpu.Name,
                    "vendor": get_gpu_vendor(gpu.PNPDeviceID) or 'N/A',
                    "vram": get_size(int(gpu.AdapterRAM)) if gpu.AdapterRAM else 'N/A',
                    "driver_version": gpu.DriverVersion or 'N/A'
                }
                data["gpu"].append(gpu_data)
        except Exception:
            data["gpu"] = [{"error": "Failed to get GPU info"}]

        # RAM
        try:
            svmem = psutil.virtual_memory()
            data["ram"]["total_gb"] = get_size(svmem.total)
            data["ram"]["modules"] = []
            ram_modules = c.Win32_PhysicalMemory()
            for module in ram_modules:
                module_data = {
                    "manufacturer": module.Manufacturer or 'N/A',
                    "capacity": get_size(int(module.Capacity)),
                    "speed_mhz": module.Speed or 'N/A',
                    "part_number": module.PartNumber.strip() if module.PartNumber else 'N/A'
                }
                data["ram"]["modules"].append(module_data)
        except Exception:
            data["ram"] = {"error": "Failed to get RAM info"}

        # Motherboard
        try:
            board = c.Win32_BaseBoard()[0]
            data["motherboard"] = {
                "manufacturer": board.Manufacturer,
                "model": board.Product,
                "serial_number": board.SerialNumber
            }
        except Exception:
            data["motherboard"] = {"error": "Failed to get Motherboard info"}

        # Storage
        try:
            disks = c.Win32_DiskDrive()
            for disk in disks:
                disk_data = {
                    "model": disk.Model,
                    "capacity": get_size(int(disk.Size)),
                    "interface_type": disk.InterfaceType
                }
                data["storage"].append(disk_data)
        except Exception:
            data["storage"] = [{"error": "Failed to get Storage info"}]

        # OS
        try:
            data["os"] = {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "architecture": platform.machine()
            }
        except Exception:
            data["os"] = {"error": "Failed to get OS info"}

    except Exception as e:
        data["general_error"] = f"Произошла общая ошибка при сборе информации: {e}. Возможно, потребуется запустить скрипт от имени Администратора."

    return json.dumps(data, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    # Используем questionary для выбора формата
    output_choice = questionary.select(
        "Выберите формат отчета:",
        choices=['Текстовый (.txt)', 'JSON (.json)'],
        default='Текстовый (.txt)'
    ).ask()

    if output_choice == 'JSON (.json)':
        final_report = get_system_info_json()
        output_filename = "specs.json"
    elif output_choice == 'Текстовый (.txt)':
        final_report = get_system_info_text()
        output_filename = "specs.txt"
    else:
        # Если пользователь отменил выбор (например, Ctrl+C)
        print("Выбор отменен. Выход.")
        sys.exit(0)

    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(final_report)
        print(f"Отчет успешно сохранен в файл '{output_filename}'")
    except Exception as e:
        print(f"Не удалось сохранить файл: {e}")
    
    print("\n" + final_report)
