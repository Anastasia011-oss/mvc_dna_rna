class SequenceModel:
    def __init__(self, seq=""):
        self.seq = seq.upper()
        self.type = self.detect_type()

    def detect_type(self):
        if "U" in self.seq and "T" in self.seq:
            return "invalid"
        elif "U" in self.seq:
            return "RNA"
        elif "T" in self.seq:
            return "DNA"
        else:
            return "unknown"

    def validate(self):
        valid_bases = {"A", "T", "G", "C", "U"}
        return all(base in valid_bases for base in self.seq)

    def gc_content(self):
        if len(self.seq) == 0:
            return 0
        gc = self.seq.count("G") + self.seq.count("C")
        return round(gc / len(self.seq) * 100, 2)

    def transcribe(self):
        if self.type != "DNA":
            return None
        return self.seq.replace("T", "U")

    def reverse_transcribe(self):
        if self.type != "RNA":
            return None
        return self.seq.replace("U", "T")

    def complement(self):
        if self.type == "DNA":
            complement_table = str.maketrans("ATGC", "TACG")
        elif self.type == "RNA":
            complement_table = str.maketrans("AUGC", "UACG")
        else:
            return None
        return self.seq.translate(complement_table)[::-1]

    def mutate(self, pos, new_base):
        if pos < 0 or pos >= len(self.seq):
            return None
        seq_list = list(self.seq)
        seq_list[pos] = new_base.upper()
        self.seq = "".join(seq_list)
        return self.seq

    def translate(self, frame=0, from_first_AUG=False):
        codon_table = {
            'AUG': 'M', 'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
            'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S', 'UAU': 'Y',
            'UAC': 'Y', 'UGU': 'C', 'UGC': 'C', 'UGG': 'W', 'UAA': '*',
            'UAG': '*', 'UGA': '*', 'CUU': 'L', 'CUC': 'L', 'CUA': 'L',
            'CUG': 'L', 'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
            'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q', 'CGU': 'R',
            'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'AUU': 'I', 'AUC': 'I',
            'AUA': 'I', 'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
            'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K', 'AGU': 'S',
            'AGC': 'S', 'AGA': 'R', 'AGG': 'R', 'GUU': 'V', 'GUC': 'V',
            'GUA': 'V', 'GUG': 'V', 'GCU': 'A', 'GCC': 'A', 'GCA': 'A',
            'GCG': 'A', 'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
            'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
        }

        if self.type == "DNA":
            seq = self.transcribe()
        else:
            seq = self.seq

        if from_first_AUG:
            start = seq.find("AUG")
            if start == -1:
                return ""
            seq = seq[start:]

        protein = ""
        for i in range(frame, len(seq) - 2, 3):
            codon = seq[i:i + 3]
            amino = codon_table.get(codon, "?")
            protein += amino
            if amino == "*":
                break
        return protein

    def find_orfs(self, min_len=30):
        seq = self.seq if self.type == "RNA" else self.transcribe()
        orfs = []
        for frame in range(3):
            for i in range(frame, len(seq) - 2, 3):
                codon = seq[i:i + 3]
                if codon == "AUG":
                    for j in range(i, len(seq) - 2, 3):
                        stop = seq[j:j + 3]
                        if stop in ("UAA", "UAG", "UGA"):
                            orf_len = j + 3 - i
                            if orf_len >= min_len:
                                orfs.append((i, j + 3, seq[i:j + 3]))
                            break
        return orfs

    def save_fasta(self, path):
        with open(path, "w") as f:
            f.write(f">Sequence\n{self.seq}\n")

    def load_fasta(self, path):
        with open(path, "r") as f:
            lines = f.readlines()
            self.seq = "".join(line.strip() for line in lines if not line.startswith(">"))
            self.type = self.detect_type()
