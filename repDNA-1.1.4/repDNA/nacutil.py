# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.3 (default, Jul  2 2020, 16:21:59)
# [GCC 7.3.0]
# Embedded file name: nacutil.py
# Compiled at: 2015-04-09 00:35:08

__author__ = 'Fule Liu'

import sys
import math
import itertools
from .util import frequency


def make_kmer_list(k, alphabet):
    try:
        return [('').join(e) for e in itertools.product(alphabet, repeat=k)]
    except TypeError:
        print('TypeError: k must be an inter and larger than 0, alphabet must be a string.')
        raise TypeError
    except ValueError:
        print('TypeError: k must be an inter and larger than 0')
        raise ValueError


def make_upto_kmer_list(k_values, alphabet):
    return_value = []
    for k in k_values:
        return_value.extend(make_kmer_list(k, alphabet))

    return return_value


def normalize_vector(normalize_method, k_values, vector, kmer_list):
    if normalize_method == 'none':
        return vector
    vector_lengths = {k: 0 for k in k_values}
    num_kmers = len(kmer_list)
    for i_kmer in range(0, num_kmers):
        kmer_length = len(kmer_list[i_kmer])
        count = vector[i_kmer]
        if normalize_method == 'frequency':
            vector_lengths[kmer_length] += count
        elif normalize_method == 'unitsphere':
            vector_lengths[kmer_length] += count * count

    if normalize_method == 'unitsphere':
        for k in k_values:
            vector_lengths[k] = math.sqrt(vector_lengths[k])

    return_value = []
    for i_kmer in range(0, num_kmers):
        kmer_length = len(kmer_list[i_kmer])
        count = vector[i_kmer]
        vector_length = vector_lengths[kmer_length]
        if vector_length == 0:
            return_value.append(0)
        else:
            return_value.append(float(count) / float(vector_length))

    return return_value


def substitute(position, letter, string):
    return_value = ''
    if position > 0:
        return_value = return_value + string[0:position]
    return_value = return_value + letter
    if position < len(string) - 1:
        return_value = return_value + string[position + 1:]
    return return_value


def compute_bin_num(num_bins, position, k, numbers):
    if num_bins == 1:
        return 0
    mean = 0
    for i in range(0, k):
        mean += float(numbers[(position + i)])

    mean /= k
    for i_bin in range(0, num_bins):
        if mean <= boundaries[k][i_bin]:
            break

    if i_bin == num_bins:
        sys.stderr.write('bin=num_bins=%d\n', i_bin)
        sys.exit(1)
    return i_bin


def make_sequence_vector(sequence, numbers, num_bins, revcomp, revcomp_dictionary, normalize_method, k_values, mismatch, alphabet, kmer_list, boundaries, pseudocount):
    kmer_counts = []
    for i_bin in range(0, num_bins):
        kmer_counts.append({})

    for k in k_values:
        seq_length = len(sequence) - k + 1
        for i_seq in range(0, seq_length):
            bin_num = compute_bin_num(num_bins, i_seq, k, numbers)
            kmer = sequence[i_seq:i_seq + k]
            if revcomp == 1:
                rev_kmer = find_revcomp(kmer, revcomp_dictionary)
                if cmp(kmer, rev_kmer) > 0:
                    kmer = rev_kmer
            if kmer in kmer_counts[bin_num]:
                kmer_counts[bin_num][kmer] += 1
            else:
                kmer_counts[bin_num][kmer] = 1
            if mismatch != 0:
                for i_kmer in range(0, k):
                    for letter in alphabet:
                        if kmer[i_kmer:i_kmer + 1] != letter:
                            neighbor = substitute(i_kmer, letter, kmer)
                            if revcomp == 1:
                                rev_kmer = find_revcomp(
                                    kmer, revcomp_dictionary)
                                if cmp(kmer, rev_kmer) > 0:
                                    kmer = rev_kmer
                            if neighbor in kmer_counts[bin_num]:
                                kmer_counts[bin_num][neighbor] += mismatch
                            else:
                                kmer_counts[bin_num][neighbor] = mismatch

    sequence_vector = []
    for i_bin in range(0, num_bins):
        for kmer in kmer_list:
            if kmer in kmer_counts[i_bin]:
                sequence_vector.append(kmer_counts[i_bin][kmer] + pseudocount)
            else:
                sequence_vector.append(pseudocount)

    return_value = normalize_vector(
        normalize_method, k_values, sequence_vector, kmer_list)
    return return_value


def read_fasta_sequence(numeric, fasta_file):
    first_char = fasta_file.read(1)
    if first_char == '':
        return ['', '']
    if first_char == '>':
        line = ''
    else:
        line = first_char
    line = line + fasta_file.readline()
    words = line.split()
    if len(words) == 0:
        sys.stderr.write('No words in header line (%s)\n' % line)
        sys.exit(1)
    id = words[0]
    first_char = fasta_file.read(1)
    sequence = ''
    while first_char != '>' and first_char != '':
        if first_char != '\n':
            line = fasta_file.readline()
            sequence = sequence + first_char + line
        first_char = fasta_file.read(1)

    clean_sequence = ''
    for letter in sequence:
        if letter != '\n':
            clean_sequence += letter

    sequence = clean_sequence
    if numeric == 0:
        clean_sequence = ''
        for letter in sequence:
            if letter != ' ':
                clean_sequence = clean_sequence + letter

        sequence = clean_sequence.upper()
    return [id, sequence]


def read_sequence_and_numbers(fasta_file, numbers_filename, numbers_file):
    fasta_id, fasta_sequence = read_fasta_sequence(0, fasta_file)
    if numbers_filename != '':
        number_id, number_sequence = read_fasta_sequence(1, number_file)
        if fasta_id != number_id:
            sys.stderr.write('Found mismatching IDs (%s != %d)\n' % (
                fasta_id, number_id))
            sys.exit(1)
        number_list = number_sequence.split()
        if len(fasta_sequence) != len(number_list):
            sys.stderr.write('Found sequence of length %d with %d numbers.\n' % (
                len(sequence), len(number_list)))
            print(sequence)
            print(numbers)
            sys.exit(1)
    else:
        number_list = ''
    return (fasta_id, fasta_sequence, number_list)


def find_revcomp(sequence, revcomp_dictionary):
    if sequence in revcomp_dictionary:
        return revcomp_dictionary[sequence]
    rev_sequence = list(sequence)
    rev_sequence.reverse()
    rev_sequence = ('').join(rev_sequence)
    return_value = ''
    for letter in rev_sequence:
        if letter == 'A':
            return_value += 'T'
        elif letter == 'C':
            return_value += 'G'
        elif letter == 'G':
            return_value += 'C'
        elif letter == 'T':
            return_value += 'A'
        elif letter == 'N':
            return_value += 'N'
        else:
            sys.stderr.write('Unknown DNA character (%s)\n' % letter)
            sys.exit(1)

    revcomp_dictionary[sequence] = return_value
    return return_value


def compute_quantile_boundaries(num_bins, k_values, number_filename):
    if num_bins == 1:
        return
    boundaries = {}
    for k in k_values:
        number_file = open(number_filename, 'r')
        all_numbers = []
        id, numbers = read_fasta_sequence(1, number_file)
        while id != '':
            number_list = numbers.split()
            num_numbers = len(number_list) - k
            for i_number in range(0, num_numbers):
                if i_number == 0:
                    sum = 0
                    for i in range(0, k):
                        sum += float(number_list[i])

                else:
                    sum -= float(number_list[(i_number - 1)])
                    sum += float(number_list[(i_number + k - 1)])
                all_numbers.append(sum / k)

            id, numbers = read_fasta_sequence(1, number_file)

        number_file.close()
        all_numbers.sort()
        boundaries[k] = {}
        num_values = len(all_numbers)
        bin_size = float(num_values) / float(num_bins)
        sys.stderr.write('boundaries k=%d:' % k)
        for i_bin in range(0, num_bins):
            value_index = int(bin_size * (i_bin + 1) - 1)
            if value_index == num_bins - 1:
                value_index = num_values - 1
            value = all_numbers[value_index]
            boundaries[k][i_bin] = value
            sys.stderr.write(' %g' % boundaries[k][i_bin])

        sys.stderr.write('\n')

    return boundaries


def cmp(a, b):
    return (a > b) - (a < b)


def make_revcomp_kmer_list(kmer_list):
    revcomp_dictionary = {}
    new_kmer_list = [kmer for kmer in kmer_list if cmp(
        kmer, find_revcomp(kmer, revcomp_dictionary)) <= 0]
    return new_kmer_list


def make_index_upto_k_revcomp(k):
    """Generate the index for revcomp and from 1 to k."""
    sum = 0
    index = [0]
    for i in range(1, k + 1):
        if i % 2 == 0:
            sum += math.pow(2, 2 * i - 1) + math.pow(2, i - 1)
            index.append(int(sum))
        else:
            sum += math.pow(2, 2 * i - 1)
            index.append(int(sum))

    return index


def make_index_upto_k(k):
    """Generate the index from 1 to k."""
    sum = 0
    index = [0]
    for i in range(1, k + 1):
        sum += math.pow(4, i)
        index.append(int(sum))

    return index


def make_index(k):
    """Generate the index just for k."""
    index = [
        0, int(math.pow(4, k))]
    return index


def make_kmer_vector(seq_list, kmer_list, rev_kmer_list, k, upto, revcomp, normalize):
    """Generate kmer vector."""
    if upto:
        index = make_index_upto_k(k)
        sum = [0] * k
        len_k = k
    else:
        index = make_index(k)
        sum = [0]
        len_k = 1
    vector = []
    for seq in seq_list:
        kmer_count = {}
        for i in range(len_k):
            sum[i] = 0
            for j in range(index[i], index[(i + 1)]):
                kmer = kmer_list[j]
                temp_count = frequency(seq, kmer)
                if revcomp:
                    rev_kmer = find_revcomp(kmer, {})
                    if kmer <= rev_kmer:
                        if kmer not in kmer_count:
                            kmer_count[kmer] = 0
                        kmer_count[kmer] += temp_count
                    else:
                        if rev_kmer not in kmer_count:
                            kmer_count[rev_kmer] = 0
                        kmer_count[rev_kmer] += temp_count
                else:
                    if kmer not in kmer_count:
                        kmer_count[kmer] = 0
                    kmer_count[kmer] += temp_count
                sum[i] += temp_count

        if revcomp:
            temp_vec = [kmer_count[kmer] for kmer in rev_kmer_list]
        else:
            temp_vec = [kmer_count[kmer] for kmer in kmer_list]
        if normalize:
            i = 0
            if not upto:
                temp_vec = [round(float(e) / sum[i], 3) for e in temp_vec]
            if upto:
                if revcomp:
                    upto_index = make_index_upto_k_revcomp(k)
                else:
                    upto_index = make_index_upto_k(k)
                j = 0
                for e in temp_vec:
                    if j >= upto_index[(i + 1)]:
                        i += 1
                    temp_vec[j] = round(float(e) / sum[i], 3)
                    j += 1

        vector.append(temp_vec)

    return vector


def diversity(vec):
    """Calculate diversity.

    :param vec: kmer vec
    :return: Diversity(X)
    """
    m_sum = sum(vec)
    from math import log
    return m_sum * log(m_sum, 2) - sum([e * log(e, 2) for e in vec if e != 0])


def id_x_s(vec_x, vec_s, diversity_s):
    """Calculate ID(X, S)

    :param vec_x: kmer X
    :param vec_s: kmer S
    :return: ID(X, S) = Diversity(X + S) - Diversity(X) - Diversity(S)
    """
    vec_x_s = [sum(e) for e in zip(vec_x, vec_s)]
    return diversity(vec_x_s) - diversity(vec_x) - diversity_s


if __name__ == '__main__':
    usage = 'Usage: fasta2matrix [options] <k> <fasta file>\n\n      Options:\n\n        -upto       Use all values from 1 up to the specified k.\n\n        -revcomp    Collapse reverse complement counts.\n\n        -normalize [frequency|unitsphere] Normalize counts to be\n                    frequencies or project onto unit sphere.  With -upto,\n                    normalization is done separately for each k.\n\n        -protein    Use an amino acid alphabet.  Default=ACGT.\n\n        -alphabet <string> Set the alphabet arbitrarily.\n\n        -mismatch <value>  Assign count of <value> to k-mers that\n                           are 1 mismatch away.\n\n        -binned <numbins> <file>  Create <numbins> vectors for each\n                                  sequence, and place each k-mer count\n                                  into the bin based upon its corresponding\n                                  mean value from the <file>.  The\n                                  <file> is in FASTA-like format, with\n                                  space-delimited numbers in place of\n                                  the sequences.  The sequences must\n                                  have the same names and be in the same\n                                  order as the given FASTA file.\n\n       -pseudocount <value>  Assign the given pseudocount to each bin.\n\n    '
    upto = 0
    revcomp = 0
    normalize_method = 'none'
    alphabet = 'ACGT'
    mismatch = 0
    num_bins = 1
    pseudocount = 0
    number_filename = ''
    sys.argv = sys.argv[1:]
    while len(sys.argv) > 2:
        next_arg = sys.argv[0]
        sys.argv = sys.argv[1:]
        if next_arg == '-revcomp':
            revcomp = 1
        elif next_arg == '-upto':
            upto = 1
        elif next_arg == '-normalize':
            normalize_method = sys.argv[0]
            sys.argv = sys.argv[1:]
            if normalize_method != 'unitsphere' and normalize_method != 'frequency':
                sys.stderr.write(
                    'Invalid normalization method (%s).\n' % normalize_method)
                sys.exit(1)
        elif next_arg == '-protein':
            alphabet = 'ACDEFGHIKLMNPQRSTVWY'
        elif next_arg == '-alphabet':
            alphabet = sys.argv[0]
            sys.argv = sys.argv[1:]
        elif next_arg == '-mismatch':
            mismatch = float(sys.argv[0])
            sys.argv = sys.argv[1:]
        elif next_arg == '-binned':
            num_bins = int(sys.argv[0])
            sys.argv = sys.argv[1:]
            number_filename = sys.argv[0]
            sys.argv = sys.argv[1:]
        elif next_arg == '-pseudocount':
            pseudocount = int(sys.argv[0])
            sys.argv = sys.argv[1:]
        else:
            sys.stderr.write('Invalid option (%s)\n' % next_arg)
            sys.exit(1)

    if len(sys.argv) != 2:
        sys.stderr.write(usage)
        sys.exit(1)
    k = int(sys.argv[0])
    fasta_filename = sys.argv[1]
    if revcomp == 1 and alphabet != 'ACGT':
        sys.stderr.write('Attempted to reverse complement ')
        sys.stderr.write('a non-DNA alphabet (%s)\n' % alphabet)
    k_values = []
    if upto == 1:
        start_i_k = 1
    else:
        start_i_k = k
    k_values = list(range(start_i_k, k + 1))
    boundaries = compute_quantile_boundaries(
        num_bins, k_values, number_filename)
    kmer_list = make_upto_kmer_list(k_values, alphabet)
    sys.stderr.write('Considering %d kmers.\n' % len(kmer_list))
    revcomp_dictionary = {}
    if revcomp == 1:
        kmer_list = make_revcomp_kmer_list(kmer_list)
    sys.stdout.write('fasta2matrix')
    for i_bin in range(1, num_bins + 1):
        for kmer in kmer_list:
            if num_bins > 1:
                sys.stdout.write('\t%s-%d' % (kmer, i_bin))
            else:
                sys.stdout.write('\t%s' % kmer)

    sys.stdout.write('\n')
    if fasta_filename == '-':
        fasta_file = sys.stdin
    else:
        fasta_file = open(fasta_filename, 'r')
    if number_filename == '':
        number_file = 0
    else:
        number_file = open(number_filename, 'r')
    id, sequence, numbers = read_sequence_and_numbers(
        fasta_file, number_filename, number_file)
    i_sequence = 1
    while id != '':
        if i_sequence % 100 == 0:
            sys.stderr.write('Read %d sequences.\n' % i_sequence)
        vector = make_sequence_vector(sequence, numbers, num_bins, revcomp, revcomp_dictionary,
                                      normalize_method, k_values, mismatch, alphabet, kmer_list, boundaries, pseudocount)
        sys.stdout.write(id)
        for element in vector:
            sys.stdout.write('\t%g' % element)

        sys.stdout.write('\n')
        id, sequence, numbers = read_sequence_and_numbers(
            fasta_file, number_filename, number_file)
        i_sequence += 1

    fasta_file.close()
