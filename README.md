# PCSpecs

A Python script to gather and display detailed information about your computer's hardware and operating system.

## Features

-   **Comprehensive System Information**: Collects data on CPU, GPU, RAM, Motherboard, Storage, and OS.
-   **Formatted Output**: Presents information in a human-readable text format.
-   **JSON Output**: Option to generate a machine-readable JSON report for programmatic use.
-   **Interactive Selection**: Uses `questionary` for an interactive command-line interface to choose the output format (text or JSON) using arrow keys.
-   **Error Handling**: Gracefully handles cases where information for certain components cannot be retrieved.

## How to Use

### 1. Prerequisites

Make sure you have Python 3 installed on your system.

### 2. Installation

Clone the repository or download the script files. Then, navigate to the script's directory in your terminal and run the `install.bat` file to install the necessary Python dependencies:

```bash
install.bat
```

### 3. Running the Script

Execute the `run.bat` file or run the `specs.py` script directly from your terminal:

```bash
python specs.py
```

The script will then prompt you to choose your desired output format (Text or JSON) using arrow keys.

### 4. Output

The generated report will be saved as `specs.txt` (for text format) or `specs.json` (for JSON format) in the same directory as the script.

## Dependencies

-   `psutil`: For system and process utilities.
-   `py-cpuinfo`: For detailed CPU information.
-   `WMI`: For Windows Management Instrumentation (WMI) access (Windows-specific).
-   `questionary`: For interactive command-line prompts.

---

# PCSpecs

Скрипт на Python для сбора и отображения подробной информации об аппаратном обеспечении и операционной системе вашего компьютера.

## Возможности

-   **Полная информация о системе**: Собирает данные о процессоре (CPU), видеокарте (GPU), оперативной памяти (RAM), материнской плате, накопителях и операционной системе.
-   **Форматированный вывод**: Представляет информацию в удобном для чтения текстовом формате.
-   **Вывод в JSON**: Возможность сгенерировать машиночитаемый отчет в формате JSON для программного использования.
-   **Интерактивный выбор**: Использует библиотеку `questionary` для интерактивного выбора формата вывода (текст или JSON) с помощью стрелок в командной строке.
-   **Обработка ошибок**: Корректно обрабатывает случаи, когда информация для определенных компонентов не может быть получена.

## Как использовать

### 1. Предварительные требования

Убедитесь, что у вас установлен Python 3.

### 2. Установка

Клонируйте репозиторий или загрузите файлы скрипта. Затем перейдите в директорию скрипта в терминале и запустите файл `install.bat` для установки необходимых зависимостей Python:

```bash
install.bat
```

### 3. Запуск скрипта

Запустите файл `run.bat` или выполните скрипт `specs.py` напрямую из терминала:

```bash
python specs.py
```

Скрипт предложит вам выбрать желаемый формат вывода (текст или JSON) с помощью стрелок.

### 4. Вывод

Сгенерированный отчет будет сохранен как `specs.txt` (для текстового формата) или `specs.json` (для формата JSON) в той же директории, что и скрипт.

## Зависимости

-   `psutil`: Для системных и процессных утилит.
-   `py-cpuinfo`: Для подробной информации о CPU.
-   `WMI`: Для доступа к Windows Management Instrumentation (WMI) (только для Windows).
-   `questionary`: Для интерактивных запросов в командной строке.