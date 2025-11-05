from colorama import Fore, Style, init

init(autoreset=True)

class ConsoleView:
    def print_menu(self):
        print(Fore.CYAN + "\n=== DNA/RNA MVC console ===")
        print(Fore.YELLOW + "1) Ввести/обновить последовательность")
        print("2) Проверить валидность")
        print("3) Транскрибировать ДНК -> РНК")
        print("4) Обратная транскрипция РНК -> ДНК")
        print("5) Комплементарная цепь")
        print("6) GC% и длина")
        print("7) Перевести в аминокислоты")
        print("8) Поиск ORF")
        print("9) Мутация")
        print("10) Сохранить в файл")
        print("11) Загрузить из файла")
        print("0) Выход")

    def prompt(self, msg):
        return input(Fore.LIGHTCYAN_EX + msg)

    def show(self, msg):
        print(Fore.WHITE + str(msg))

    def success(self, msg):
        print(Fore.GREEN + str(msg))

    def error(self, msg):
        print(Fore.RED + str(msg))

    def show_sequence(self, model):
        if model.seq:
            seq_type = "DNA" if "T" in model.seq else "RNA"
            print(Fore.MAGENTA + f"\nТекущая последовательность ({seq_type}):")
            print(Fore.WHITE + model.seq)
            print(Fore.YELLOW + f"Длина: {len(model.seq)}")
        else:
            self.error("\nПоследовательность не задана.")
