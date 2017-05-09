from . import _Getch
from . import INTERVALS
from . import DEBUG
# this is for debugging


def print_stuff(question):
    padd = "─" * 30  # vim: insert mode, ^vu2500
    print("""
{}

Tonic: {} | Note(Int): {} |  Interval: {} | Semitones(Int): {} |
Is Note Chromatic: {} |
Scale: {}, Octave: {}
Resolution: ,
Chromatic: {}
Concrete Scale: {} | Chroma Concrete: {}
{}
""".format(
        padd,
        question.concrete_tonic,
        question.interval['note_and_octave'],
        "─".join(INTERVALS[question.interval['semitones']][1:]),
        question.interval['semitones'],
        question.interval['is_chromatic'],
        "─".join(question.scales['diatonic'].scale),
        "{}-{}".format(question.octave, question.octave + 1),
        # "─".join(question.resolution_pitch),
        "─".join(question.scales['chromatic'].scale),
        "─".join(question.scales['diatonic_pitch'].scale),
        "─".join(question.scales['chromatic_pitch'].scale),
        padd,
    ))


def print_stuff_dictation(question):
    padd = "─" * 30  # vim: insert mode, ^vu2500
    print("""
{}

Tonic: {} | Note(Int): {} |  Interval: {} | Semitones(Int): {} |
Scale: {}, Octave: {}
Chromatic: {}
Concrete Scale: {} | Chroma Concrete: {}
{}
""".format(
        padd,
        question.concrete_tonic,
        "─".join(map(str, question.question_phrase)),
        "─".join([INTERVALS[n][1] for n in question.question_phrase]),
        "─".join([str(n) for n in question.question_phrase]),
        "─".join(question.scales['diatonic'].scale),
        "{}-{}".format(question.octave, question.octave + 1),
        "─".join(question.scales['chromatic'].scale),
        "─".join(question.scales['diatonic_pitch'].scale),
        "─".join(question.scales['chromatic_pitch'].scale),
        padd,
    ))

# dictate_notes = 4
#
#
# def main():
#     from .questions.melodicdictation import MelodicDictationQuestion
#     getch = _Getch()
#
#     new_question_bit = True
#
#     while True:
#         if new_question_bit is True:
#
#             new_question_bit = False
#
#             input_keys = []
#             # question = MelodicDictateQuestion(mode='major',descending=True)
#             question = MelodicDictationQuestion(mode='major')
#             # question = HarmonicIntervalQuestion(mode='major')
#             # question = HarmonicIntervalQuestion(mode='major')
#
#             # debug
#             if DEBUG:
#                 print_stuff_dictation(question)
#
#             question.question.play()
#
#         user_input = getch()
#
#         # any response input interval from valid keys
#         if user_input in question.keyboard_index and user_input != ' ':  # spc
#
#             input_keys.append(user_input)
#             print(user_input, end='')
#
#             if len(input_keys) == dictate_notes:
#                 # response = question.check_question(user_input)
#                 response = question.check_question(input_keys)
#
#                 if response['is_correct']:
#                     # print("Correct!.. it is “{}”".\
#                     # format( response['user_interval']))
#                     print("Correct! It was semitones {}".
#                           format("-".join(map(str, question.question_phrase))))
#                 else:
#                     print("It is incorrect...")
#                     print("You replied semitones {} but the correct is "
#                           "semitones {}".format(response['user_semitones'],
#                                                 question.question_phrase))
#
#                 question.resolution.play()
#
#                 new_question_bit = True
#             # else:
#             #    input_keys.append(user_input)
#             #    print(user_input,)
#
#         # q - quit
#         elif user_input == 'q':
#             exit(0)
#
#         # r - repeat interval
#         elif user_input == 'r':
#             question.question.play()

wait_keys = 1
def main():

    from .questions.harmonicinterval import HarmonicIntervalQuestion
    from .questions.melodicinterval import MelodicIntervalQuestion
    getch = _Getch()

    new_question_bit = True

    while True:
        if new_question_bit is True:

            new_question_bit = False

            input_keys = []
            question = HarmonicIntervalQuestion(mode='major')
            #question = MelodicIntervalQuestion(mode='major',descending=True)
            #question = MelodicIntervalQuestion(mode='major')

            # debug
            if DEBUG:
                print_stuff(question)

            question.question.play()

        user_input = getch()

        if user_input in question.keyboard_index:
            response = question.check_question(user_input)

            if response['is_correct']:
                print("Correct!.. it is “{}”".\
                format( response['user_interval']))
            else:
                print("It is incorrect... correct is {}.. you said {}".\
                       format(question.interval['data'],
                              response['user_interval']))

            question.resolution.play()

            new_question_bit = True

        # q - quit
        elif user_input == 'q':
            exit(0)

        # r - repeat interval
        elif user_input == 'r':
            question.question.play()

if __name__ == "__main__":
    main()
