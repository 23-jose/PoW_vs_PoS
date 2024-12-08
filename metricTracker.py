import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def getMetrics(filePath):
    with open(filePath, 'r') as file:
        metricsText = file.readlines()

    timeList = []
    cpuUsageList = []
    memoryUsageList = []
    diskReadList = []
    diskWriteList = []
    networkInList = []
    networkOutList = []
    
    timeDataFormat = r"\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}"
    cpuDataFormat = r"CPU usage: (\d+\.\d+)%"
    memoryDataFormat = r"PhysMem: (\d+M)"
    diskDataFormat = r"Disks: (\d+/\d+G) read, (\d+/\d+G) written"
    networkDataFromat = r"Networks: packets: (\d+/[0-9\.]+G) in, (\d+/[0-9\.]+M) out"
    
    for line in metricsText:

        timeCheck = re.search(timeDataFormat, line)
        if timeCheck:
            timeList.append(datetime.strptime(timeCheck.group(), "%Y/%m/%d %H:%M:%S"))
        
        cpuCheck = re.search(cpuDataFormat, line)
        if cpuCheck:
            cpuUsageList.append(float(cpuCheck.group(1)))
        
        memoryCheck = re.search(memoryDataFormat, line)
        if memoryCheck:
            memoryUsageList.append(int(memoryCheck.group(1).replace("M", "")))
        
        diskCheck = re.search(diskDataFormat, line)
        if diskCheck:
            raed = diskCheck.group(1).split('/')[0]
            write = diskCheck.group(2).split('/')[0]
            diskReadList.append(int(raed.replace("G", "")))
            diskWriteList.append(int(write.replace("G", "")))
        
        networkCheck = re.search(networkDataFromat, line)
        if networkCheck:
            In = networkCheck.group(1).split('/')[0]
            Out = networkCheck.group(2).split('/')[0]
            networkInList.append(float(In.replace("G", "")))
            networkOutList.append(float(Out.replace("M", "")))

    data = {
        'Timestamp': timeList,
        'CPU Usage (%)': cpuUsageList,
        'Memory Usage (MB)': memoryUsageList,
        'Disk Read (GB)': diskReadList,
        'Disk Write (GB)': diskWriteList,
        'Network In (GB)': networkInList,
        'Network Out (GB)': networkOutList
    }
    
    data['Elapsed Time (s)'] = [(timestamp - timeList[0]).total_seconds() for timestamp in timeList]

    return pd.DataFrame(data)

def graph(df, label):
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 2, 1)
    plt.plot(df['Elapsed Time (s)'], df['CPU Usage (%)'], label=f"{label} CPU Usage", color='orange')
    plt.xlabel('Elapsed Time (s)')
    plt.ylabel('CPU Usage (%)')
    plt.title(f'{label} CPU Usage Over Time')

    plt.subplot(2, 2, 2)
    plt.plot(df['Elapsed Time (s)'], df['Memory Usage (MB)'], label=f"{label} Memory Usage", color='blue')
    plt.xlabel('Elapsed Time (s)')
    plt.ylabel('Memory Usage (MB)')
    plt.title(f'{label} Memory Usage Over Time')

    plt.subplot(2, 2, 3)
    plt.plot(df['Elapsed Time (s)'], df['Disk Read (GB)'], label=f"{label} Disk Read", color='green')
    plt.plot(df['Elapsed Time (s)'], df['Disk Write (GB)'], label=f"{label} Disk Write", color='red')
    plt.xlabel('Elapsed Time (s)')
    plt.ylabel('Disk Usage (GB)')
    plt.title(f'{label} Disk Read/Write Over Time')

    plt.subplot(2, 2, 4)
    plt.plot(df['Elapsed Time (s)'], df['Network In (GB)'], label=f"{label} Network In", color='purple')
    plt.plot(df['Elapsed Time (s)'], df['Network Out (GB)'], label=f"{label} Network Out", color='brown')
    plt.xlabel('Elapsed Time (s)')
    plt.ylabel('Network Traffic (GB)')
    plt.title(f'{label} Network In/Out Over Time')

    plt.tight_layout()
    plt.legend(loc='upper left')
    plt.show()

def main():
    bitcoinFile = "bitcoin_metrics.txt"
    ethereumFile = "geth_sepolia_metrics.txt"
    
    bitcoinMetrics = getMetrics(bitcoinFile)
    ethereumMetrics = getMetrics(ethereumFile)
    
    graph(bitcoinMetrics, "Bitcoin (PoW)")
    graph(ethereumMetrics, "Ethereum (PoS)")

if __name__ == "__main__":
    main()
