from rouge import Rouge

hypothesis1 = "the #### transcript is a written version of each day 's cnn student news program use this transcript " \
              "to he    lp students with reading comprehension and vocabulary use the weekly newsquiz to test your " \
              "knowledge of storie s you     saw on cnn student news "
reference1 = "this page includes the show transcript use the transcript to help students with reading comprehension " \
             "and     vocabulary at the bottom of the page , comment for a chance to be mentioned on cnn student news " \
             ". you must be a teac    her or a student age # # or older to request a mention on the cnn student news " \
             "roll call . the weekly newsquiz tests     students ' knowledge of even ts in the news "

hypothesis2 = "Tokyo is the one of the biggest city in the world."
reference2 = "Tokyo is the one of the biggest city in the world."
rouge = Rouge()
scores1 = rouge.get_scores(hypothesis1, reference1)
print(scores1)
scores2 = rouge.get_scores(hypothesis2, reference2)
print(scores2)
