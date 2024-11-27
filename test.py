import src.llm_interface as li

ans,sources = li.get_explanation_with_sources(
    mcq_question='An individual who has consumed a moderate amount of alcohol prior to sleep is likely to have:',
    correct_answer='less REM sleep',
    answer_seeking_explanation='a longer sleep'
)

print('ANSWER:')
print(ans)
print('SOURCES:')
for source in sources:
    print(source)
