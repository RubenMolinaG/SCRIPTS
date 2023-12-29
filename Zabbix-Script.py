import sys
import datetime

def number_of_arguments_is_valid(args_number: int) -> bool:
    match args_number:
        case 0:
            print("[ERROR] - No argument was introduced.")
            print("Usage Example: Zabbix-Script.py ./CSV_FILE.csv")
            return False
        case 1:
            return True
        case other:
            print("[ERROR] - More than one argument was introduced.")
            print("Usage Example: Zabbix-Script.py ./CSV_FILE.csv")
            return False

def extract_nodes_from_csv_file(csv_file_path: str) -> list[str]:
    list_nodes: list[str] = list()
    try:
        with open(csv_file_path, 'r') as csv_file:
            for line in csv_file:
                node = line.split(",")[4]
                if "h12" in node or "ad0" in node:
                    list_nodes.append(node)
    except FileNotFoundError as e:
        print(f"[ERROR] - File '{csv_file_path}' NOT found.")
        print(e)
        sys.exit(1)
    return list_nodes
    
def create_nodes_dict(nodes_list: list[str]) -> dict[str, int]:
    dict_nodes: dict[str, int] = dict()
    for node in nodes_list:
        dict_nodes[node] = 0
    return dict_nodes

def number_times_host_appears(nodes_list: list[str], nodes_dict: dict[str, int]) -> dict[str, int]:
    _nodes_list = nodes_list
    _nodes_dict = nodes_dict
    for node in _nodes_list:
        if node in _nodes_dict.keys():
            _nodes_dict[node] += 1
    return _nodes_dict

def sort_nodes_dict(unsorted_nodes_dict: dict[str, int]) -> list[tuple[str, int]]:
    return sorted(unsorted_nodes_dict.items(), key=lambda x:x[1], reverse=True)

def write_sorted_dict_file(list_sorted_nodes: list[ tuple[str, int] ]) -> None:
    DATE: datetime = datetime.datetime.now()
    FILE_NAME: str = f"Zabbix-Nodes-{DATE.year}{DATE.month}{DATE.day}.txt"
    with open(FILE_NAME, 'w') as file:
        for line in list_sorted_nodes:
            node: str = line[0]
            occurrences: int = line[1]
            file.write(f"{node}: {occurrences}\n")
    print(f"File '{FILE_NAME}' created successfully..")

def main():
    if not number_of_arguments_is_valid(len(sys.argv[1:])):
        sys.exit(1)

    CSV_FILE_PATH = sys.argv[1]
    list_nodes: list[str] = extract_nodes_from_csv_file(CSV_FILE_PATH)
    
    dict_unsorted_nodes: dict[str, int] = number_times_host_appears(
        list_nodes, 
        create_nodes_dict(list_nodes))
    
    dict_sorted_nodes: list[tuple[str, int]] = sort_nodes_dict(dict_unsorted_nodes)

    write_sorted_dict_file(dict_sorted_nodes)
    
if __name__ == '__main__':
    main()
