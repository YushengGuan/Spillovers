# execute this file to run all figure generation programmes。
import subprocess


def run_file(name):
    result = subprocess.run(['python', name])
    if result.returncode == 0:
        print(f"{name} executed successfully")
    else:
        print("Error executing other_script.py")
    return result.returncode


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    run_file('Regressions.py')
    for i in range(1, 6):
        run_file(f'Figure_{i}.py')
    for i in range(1, 12):
        if i != 7:  # manually drawn
            run_file(f'Figure_S{i}.py')
