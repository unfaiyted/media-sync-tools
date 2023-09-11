


class AiProvider:

    media_list = []

    format_str_movies = f'{{"Movies": [{{"name": "Movie Name", "year": "Movie Year"}}]}}'
    format_str_series = f''
    format_str_episodes = f''

    retry_count = 3

    model="gtp-3.5-turbo"

    default_messages=[
        {"role": "system",
        "content": f"I respond with json objects."}
    ]

    def __init__(self, media_types,  description, filters=None, limit=25):
        self.media_types = media_types
        self.limit = limit
        self.filters = filters
        self.description = description



# Goal is to be able to take in a ListBuilder object and return a List of media files that could be used to
    # create either a list of some kind.

#    def _parse_filters(self):
#        # take the filters and make each one a human readable string
#
#
#    rules = f'Return a json object with the format {format_str}.' \
#            f'Provide a list of {count} movies that I have not seen. ' \
#            f'Only recommend {media_type}.'
#


    def _get_limit_rule(self, limit):
        return f'Respond with {limit} items.'
    def _get_media_type_rule(self):
        # if more than one change phrasing
        return 'Only recommend Movies.'

    def _get_json_format_rule(self):
        # figure out what media type/s and respond accordingly

        return f"json format........"

    def _get_chat_res_as_json(self, rules, movies=None, retry_count=0):
           if (retry_count > self.retry_count):
               print("Failed to get chat as json.")
           return None

           if movies is None:
               movie_content = f'Suggest movies to watch. Following the rules: {rules}'
           else:
               movie_content = f"Based on this list of movies: {movies}. Suggest more movies to watch."

           completion = self.chat.ChatCompletion.create(model="gpt-3.5-turbo",
           messages=[
                         {"role": "system",
                         "content": f"I will ALWAYS respond with a json object and no text oustide of that object. \n {rules}"},
                         {"role": "user", "content": movie_content}
                            ])
           response = completion.choices[0].message.content

           # print(response)

           try:
               return json.loads(response)
           except Exception as e:
               print(f"Message not in json format. Retrying... {retry_count} of 3")
           # try again...
           time.sleep(20)  # max 3 req per min
           return self._convert_res_to_json(response, rules, retry_count + 1)

   # def _convert_media_list_to_names_as_csv(self, media_list):
   #                                                                names = ''
   #                                                                for media in media_list:
   #                                                                names += media['Name'] + ', '
   #
   #                                                                return names

    # def _convert_res_to_json(self, response, rules, retry_count=0):
    #                                                                    if (retry_count > 2):
    #                                                                    print("Failed to get chat as json.")
    #                                                                    return None
    #
    #                                                                    try:
    #                                                                    completion = self.chat.ChatCompletion.create(
    #                                                                    model="gpt-3.5-turbo",
    #                                                                    messages=[
    #                                                                    {"role": "system",
    #                                                                    "content": f"I will ALWAYS respond with a json object and no text oustide of that object. \n {rules}"},
    #                                                                    {"role": "user", "content": f"Convert this list to a json object: {response} \n {rules} "}
    #
    #                                                                    ])
    #
    #                                                                    print(completion.choices[0].message.content)
    #
    #                                                                    return json.loads(completion.choices[0].message.content)
    #                                                                    except:
    #                                                                    print(f"Message still not in json format. ")
    #                                                                    # try again...



    # def get_media_list(self):


