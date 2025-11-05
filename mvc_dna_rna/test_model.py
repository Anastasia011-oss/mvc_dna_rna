import pytest
from model import SequenceModel


def test_validate_dna():
    seq = SequenceModel("ATGC")
    assert seq.validate() is True
    assert seq.type == "DNA"


def test_validate_rna():
    seq = SequenceModel("AUGC")
    assert seq.validate() is True
    assert seq.type == "RNA"


def test_invalid_sequence():
    seq = SequenceModel("ATXG")
    assert seq.validate() is False
    assert seq.type == "unknown"


def test_gc_content():
    seq = SequenceModel("GGCCAA")
    assert round(seq.gc_content(), 2) == 66.67


def test_transcription():
    dna = SequenceModel("ATGC")
    assert dna.transcribe() == "AUGC"


def test_reverse_transcription():
    rna = SequenceModel("AUGC")
    assert rna.reverse_transcribe() == "ATGC"


def test_complement():
    dna = SequenceModel("ATGC")
    assert dna.complement() == "GCAT"


def test_mutate():
    dna = SequenceModel("ATGC")
    dna.mutate(1, "A")
    assert dna.seq == "AAGC"


def test_translate_stop():
    rna = SequenceModel("AUGGCCUAA")
    assert rna.translate() == "MA"


def test_find_orfs():
    seq = SequenceModel("AUGGCCUAAUGA")
    orfs = seq.find_orfs()
    assert len(orfs) >= 1
    assert orfs[0][3].startswith("MA")
