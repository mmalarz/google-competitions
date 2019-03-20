import itertools


TEST_FILE_NAME = 'A-small-practice.in'
STRING_TO_INT_NUMBERS_MAPPING = {
    '1111011': 9,
    '1111111': 8,
    '1110000': 7,
    '1011111': 6,
    '1011011': 5,
    '0110011': 4,
    '1111001': 3,
    '1101101': 2,
    '0110000': 1,
    '1111110': 0,
}
INT_TO_STRING_NUMBERS_MAPPING = {
    9: '1111011',
    8: '1111111',
    7: '1110000',
    6: '1011111',
    5: '1011011',
    4: '0110011',
    3: '1111001',
    2: '1101101',
    1: '0110000',
    0: '1111110',
}


def get_possibly_broken_segments(number_list):
    """
    Gets all switched off segments that are common for all the digits.
    """
    empty_segments = list()
    number_count = len(number_list)

    for number_string in number_list:
        for position, char in enumerate(number_string):
            if char == '0':
                empty_segments.append(position)

    return {
        segment for segment in empty_segments
        if empty_segments.count(segment) == number_count
    }


def get_possible_numbers(number_list, available_segments):
    """
    Gets all possible combinations of digits
    that you can create from given list of strings
    """
    possible_numbers = list()
    available_segments = list(available_segments)

    for index, number_string in enumerate(number_list):
        possible_numbers.append(list())
        if number_string in STRING_TO_INT_NUMBERS_MAPPING:
            possible_numbers[index].append(
                STRING_TO_INT_NUMBERS_MAPPING[number_string]
            )

        for comb_len in range(1, len(available_segments) + 1):
            for position_list_comb in itertools.combinations(available_segments, comb_len):
                new_number_string = list(number_string)

                for position in position_list_comb:
                    new_number_string[position] = '1'

                new_number_string = ''.join(new_number_string)
                if new_number_string in STRING_TO_INT_NUMBERS_MAPPING:
                    possible_numbers[index].append(
                        STRING_TO_INT_NUMBERS_MAPPING[new_number_string]
                    )

    return possible_numbers


def filter_out_possible_numbers(possible_numbers):
    sorted_list = list()
    bad_numbers = list()
    possible_numbers_last_index = len(possible_numbers) - 1
    change = 1

    if len(possible_numbers) == 1:
        return bad_numbers, possible_numbers[0] if len(possible_numbers[0]) == 1 else []

    for index, number_list in enumerate(possible_numbers):
        for number in number_list:
            if index == possible_numbers_last_index:
                change = -1
            else:
                change = 1

            if number == 0:
                mapping = {
                    0: 9 in possible_numbers[index + change],
                }
            else:
                mapping = {
                    number: number - change in possible_numbers[index + change],
                }

            if mapping[number]:
                print(f'{number} SEEMS OK, ADDING!')
                sorted_list.append(number)
            else:
                print(f'{number} DON\'T LIKE IT, MARKING!')
                bad_numbers.append(number)
        print('-')

    return bad_numbers, sorted_list if len(sorted_list) == len(possible_numbers) else []


def get_next_number(broken_segments, last_number):
    if last_number not in range(0, 10):
        return 'ERROR!'

    mapping = {
        9: '1111110',
        0: '1111011',
    } 
    next_number = list(
        mapping[last_number]
        if last_number in [0, 9]
        else INT_TO_STRING_NUMBERS_MAPPING[last_number - 1]
    )

    for segment in broken_segments:
        next_number[segment] = '0'

    return ''.join(next_number)


def main():
    i = 1
    with open(TEST_FILE_NAME) as test_file:
        for line in test_file.readlines()[1:]:
            num_list = line.split()[1:]
            av_seg = get_possibly_broken_segments(num_list)
            pos_nums = get_possible_numbers(num_list, av_seg)
            bad_numbers, sorted_list = filter_out_possible_numbers(pos_nums)
            last_num = sorted_list[-1] if sorted_list else ''
            next_num = get_next_number(av_seg, last_num)
            print(num_list)
            print(f'Possibly broken segments: {av_seg}')
            print(f'Possible numbers: {pos_nums}')
            print(f'Selected numbers: {sorted_list}')
            print(f'Bad numbers: {bad_numbers}')
            print(f'Last num: {last_num}')
            print(f'Next num: {next_num}')
            print('-' * 80)
            # print(f'Case #{i}: {next_num}')
            i += 1


if __name__ == '__main__':
    main()
