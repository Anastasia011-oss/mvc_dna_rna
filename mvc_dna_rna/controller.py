from model import SequenceModel
from view import ConsoleView


class Controller:
    def __init__(self):
        self.model = SequenceModel()
        self.view = ConsoleView()

    def run(self):
        while True:
            self.view.print_menu()
            choice = self.view.prompt("Выберите пункт меню: ")

            commands = {
                "1": self.cmd_input_seq,
                "2": self.cmd_validate,
                "3": self.cmd_transcribe,
                "4": self.cmd_rev_transcribe,
                "5": self.cmd_rev_comp,
                "6": self.cmd_gc_len,
                "7": self.cmd_translate,
                "8": self.cmd_orf,
                "9": self.cmd_mutate,
                "10": self.cmd_save,
                "11": self.cmd_load,
                "0": self.cmd_exit
            }

            cmd = commands.get(choice)
            if cmd:
                cmd()
            else:
                self.view.error("Неверный выбор, попробуйте снова.")

    def cmd_input_seq(self):
        seq = self.view.prompt("Введите последовательность ДНК или РНК: ").strip().upper()
        self.model = SequenceModel(seq)
        self.view.success(f"Последовательность сохранена: {self.model.seq}")

    def cmd_validate(self):
        if not self.model.seq:
            self.view.error("Нет последовательности!")
            return
        if self.model.validate():
            self.view.success(f"Последовательность корректна ({self.model.type}).")
        else:
            self.view.error("Ошибка: недопустимые символы.")

    def cmd_transcribe(self):
        result = self.model.transcribe()
        if result:
            self.view.success(f"РНК: {result}")
        else:
            self.view.error("Это не ДНК! Транскрипция невозможна.")

    def cmd_rev_transcribe(self):
        result = self.model.reverse_transcribe()
        if result:
            self.view.success(f"ДНК: {result}")
        else:
            self.view.error("Это не РНК! Обратная транскрипция невозможна.")

    def cmd_rev_comp(self):
        result = self.model.complement()
        if result:
            self.view.success(f"Комплементарная цепь: {result}")
        else:
            self.view.error("Ошибка: невозможно построить цепь.")

    def cmd_gc_len(self):
        if not self.model.seq:
            self.view.error("Сначала введите последовательность!")
            return
        gc = self.model.gc_content()
        length = len(self.model.seq)
        self.view.success(f"GC-состав: {gc:.2f}% | Длина: {length}")

    def cmd_translate(self):
        result = self.model.translate()
        if result:
            self.view.success(f"Аминокислотная последовательность: {result}")
        else:
            self.view.error("Ошибка: не удалось выполнить трансляцию.")

    def cmd_orf(self):
        orfs = self.model.find_orfs()
        if not orfs:
            self.view.error("ORF не найдены.")
        else:
            self.view.success("Найденные ORF:")
            for start, end, seq in orfs:
                self.view.show(f"{start}-{end}: {seq}")

    def cmd_mutate(self):
        if not self.model.seq:
            self.view.error("Сначала введите последовательность!")
            return
        try:
            pos = int(self.view.prompt("Введите позицию мутации (0-индексация): "))
            new_base = self.view.prompt("Введите новую букву: ").upper()
            result = self.model.mutate(pos, new_base)
            if result:
                self.view.success(f"Мутация выполнена: {self.model.seq}")
            else:
                self.view.error("Ошибка: позиция вне диапазона.")
        except ValueError:
            self.view.error("Ошибка: введите целое число!")

    def cmd_save(self):
        path = self.view.prompt("Введите имя файла для сохранения (.fasta): ")
        try:
            self.model.save_fasta(path)
            self.view.success(f"Сохранено в {path}")
        except Exception as e:
            self.view.error(f"Ошибка при сохранении: {e}")

    def cmd_load(self):
        path = self.view.prompt("Введите имя файла для загрузки (.fasta): ")
        try:
            self.model.load_fasta(path)
            self.view.success(f"Последовательность загружена: {self.model.seq}")
        except FileNotFoundError:
            self.view.error("Файл не найден.")

    def cmd_exit(self):
        self.view.show("Выход из программы.")
        exit()
