import re

import trello

import CONFIG
import bot_responses

# Checks the blacklist for passed in user name
def check_user_in_blacklist(UserName):
    # The escaping is removed so both fancy pants and markdown editor have same text
#    output = UserName.replace("\\", "")

    blacklist_result = list()
    blacklist_result.append(search_in_blacklist(UserName.strip()))

    return bot_responses.blacklist_search_result_for_query(UserName, blacklist_result)

# Removes the archived cards from list
def delete_archived_cards_and_check_desc(search_result, search_query):
    for card in search_result:
        # Some search query returns the boards and the members which creates issue later
        if card.__class__ != trello.Card:
            search_result.remove(card)
            continue
        # closed means the card is archived
        if card.closed:
            search_result.remove(card)
        # Double check to make sure that search query is in card description
        if search_query.lower() not in card.description.lower().replace("\\", ""):
            search_result.remove(card)
    return search_result

# Searches in trello board using trello api and return the search result in a list\
# The list is empty if there are no search results
def search_in_blacklist(search_query):
    search_result = list()
    try:
        # escapes the special characters so the search result is exact not from wildcard (e.g '-')
        search_result = CONFIG.trello_client.search(query=re.escape(search_query), cards_limit=10)
        search_result_escaped_underscore = list()
        # If underscore is in search query, we need to search it escaped and non escaped
        if "_" in search_query:
            search_result_escaped_underscore = CONFIG.trello_client.search(
                query=re.escape(search_query.replace("_", "\\_")), cards_limit=10)
        # Adding results from both searches
        search_result = search_result + search_result_escaped_underscore
        # Removing duplicate search results
        search_result = list(set(search_result))
        search_result = delete_archived_cards_and_check_desc(search_result, search_query)
    except NotImplementedError:
        raise NotImplementedError(search_query)
    return search_result