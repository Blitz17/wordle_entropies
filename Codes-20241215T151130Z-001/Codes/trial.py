import ast
# d = {}
# with open("output_answer_hard.txt", "r", encoding="utf8") as file :
#     lines = file.readlines()
#     set_2 = set()
#     for line in lines :
#         line_list = ast.literal_eval(line)
#         print(line_list[3][1])
#         set_2.add(line_list[3][1])
#         if (line_list[3][1] in d):
#             d[line_list[3][1]] += 1
#         else :
#             d[line_list[3][1]] = 1
#     print(set_2)
#     print(len(set_2))
#     print('d ' + str(d))
#     print(type(d))

# d = {1 : 'abc'}
# d[2] = 'dgc'
# print(1 in d)
# print(d[1])
# print(d[2])
if True:
        results = [-1] * len('jetty')
        answer_letter_count = {}   

        for i in range(len('jetty')):
            if 'jetty'[i] == 'attic'[i]:
                results[i] = 1
            else:
                if 'attic'[i] in answer_letter_count:
                    answer_letter_count['attic'[i]] += 1
                else:
                    answer_letter_count['attic'[i]] = 1
        
        for i in range(len('jetty')):
            if results[i] != 1:  # Only check non-green letters
                if 'jetty'[i] in answer_letter_count and answer_letter_count['jetty'[i]] > 0:
                    results[i] = 0
                    answer_letter_count['jetty'[i]] -= 1

        print(results)