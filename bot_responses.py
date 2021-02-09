# Get all labels from the trello card
def get_all_labels(trello_card):
    # If there are no labels for card
    if trello_card.labels is None:
        return "BLACKLISTED"
    # Otherwise return all label names in string
    labels = ""
    for label in trello_card.labels:
        labels += label.name + ", "
    return labels[:-2]


# Comments the blacklist search result for search queries that are requested by the users
def blacklist_search_result_for_query(user_name, blacklist):
    response_text = ""
    usernames_for_positive_result = ""  # stores the usernames which gave positive search result in string
    positive_result_usernames_list = []  # stores the usernames which gave positive search result in list
    positive_results = []  # # stores the results of positive result usernames
    negative_results_usernames_list = []  # stores the usernames which gave negative search result in string
    usernames_for_negative_result = ""  # stores the usernames which gave negative search result in list
    # Iterate over each user name in query list
    # If that username gave positive search result
    i = 0
    if len(blacklist[i]) > 0:
        usernames_for_positive_result += user_name + ", "
        positive_result_usernames_list.append(user_name)
        positive_results.append(blacklist[i])
        # If that username gave negative search result
    else:
        usernames_for_negative_result += user_name + ", "
        negative_results_usernames_list.append(blacklist[i])
    # If there are users that had positive search result
    if len(positive_result_usernames_list) > 0:
        response_text += "The user *\"" + usernames_for_positive_result[:-2] + "\"* has been found on the blacklist. "
        response_text += "The links for each time the user appeared in the blacklist are:\n\n"
        # Iterate over each user
        for i in range(len(positive_result_usernames_list)):
            # Iterate over that user's trello search result as result could have multiple cards
            for positive_result in positive_results[i]:
                response_text = response_text + get_all_labels(positive_result) + ": " + positive_result.name + \
                                " **(" + positive_result_usernames_list[
                                    i] + ")**\n\n" + positive_result.short_url + "\n\n"
        response_text = response_text + "^(Please check each link to verify)\n\n"
    # If there are users that had negative search result
    if len(negative_results_usernames_list) > 0:
        response_text += "The bot has performed a search and has determined that the user *\""
        response_text += usernames_for_negative_result[:-2]
        response_text += "\"* is not in present in our blacklist."
    return response_text
